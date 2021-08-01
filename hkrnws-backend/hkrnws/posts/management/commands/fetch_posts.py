import pytz
from datetime import datetime
from lxml import etree
from urllib.request import urlopen
from django.core.management.base import BaseCommand

from hkrnws.posts.models import Post, CrawlRun


class Command(BaseCommand):
    help = 'Scrape and save posts from first 3 pages of Hackernews'

    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.scrape()


class Scraper():

    def __init__(self):
        self.post_url = None
        self.post_string = None
        self.post_points = None
        self.post_timestamp = None
        self.time_posted_ago = None
        self.post_subtext = None
        self.post_subtext_links = None
        self.special_posts_idx = None
        self.tree = None
        self.scraped_hn_post_ids = []
        self.scraped_posts = []

    def scrape(self):
        for i in range(1,4):
            url = f"https://news.ycombinator.com/news?p={i}"
            response = urlopen(url)
            htmlparser = etree.HTMLParser()
            self.tree = etree.parse(response, htmlparser)
            self.scraped_posts.extend(self.scrape_post_data())
        self.update_or_create_posts()

    def update_or_create_posts(self):
        try:
            crawl_run_instance = CrawlRun()
            crawl_run_instance.save()

            # Filter Posts to Update or Create new
            posts_dict = {int(post['hn_id']):post for post in self.scraped_posts}
            post_ids_to_update = list(Post.objects.filter(pk__in=self.scraped_hn_post_ids).values_list('id', flat=True))
            posts_to_update = Post.objects.filter(pk__in=post_ids_to_update)
            
            # Update posts with new points, comments and crawler ID
            for post in posts_to_update:
                post.points = posts_dict[post.id]['points']
                post.comments = posts_dict[post.id]['comments']
                post.crawl_run = crawl_run_instance
            updated_posts = Post.objects.bulk_update(posts_to_update, ['points', 'comments', 'crawl_run'])
            crawl_run_instance.posts_updated = len(post_ids_to_update)
            crawl_run_instance.save()

            # Create new posts
            posts_to_create = []
            utc = pytz.timezone('UTC')
            for id in self.scraped_hn_post_ids:
                if id not in post_ids_to_update:
                    post = Post(
                        id = posts_dict[id]['hn_id'],
                        title = posts_dict[id]['title'],
                        story_url = posts_dict[id]['story_url'],
                        timestamp = utc.localize(datetime.strptime(posts_dict[id]['timestamp'], '%Y-%m-%dT%H:%M:%S')),
                        points = posts_dict[id]['points'],
                        posted_by = posts_dict[id]['username'],
                        comments = posts_dict[id]['comments'],
                        poster_profile_url = posts_dict[id]['user_profile_url'],
                        hn_post_url = posts_dict[id]['hn_post_url'],
                        crawl_run = crawl_run_instance
                    )
                    posts_to_create.append(post)
            created_posts = Post.objects.bulk_create(posts_to_create)    
            crawl_run_instance.posts_updated = 0 if created_posts == None else len(created_posts)
            crawl_run_instance.save()

        except Exception as e:
            raise e

    def scrape_post_data(self):
        # Post URL
        self.post_url = self.tree.xpath('//td[@class="title"]/a/@href')
        # Post title 
        self.post_string = self.tree.xpath('//td[@class="title"]/a/text()')
        # Post points
        self.post_points = self.tree.xpath('//span[@class="score"]/text()')
        # Timestamps
        self.post_timestamp = self.tree.xpath('//span[@class="age"]/@title')
        # Time posted ago
        self.time_posted_ago = self.tree.xpath('//span[@class="age"]/a/text()')
        # Subtext string
        self.post_subtext = self.tree.xpath('//td[@class="subtext"]/a/text()')
        # same as above but links
        self.post_subtext_links = self.tree.xpath('//td[@class="subtext"]/a/@href')

        self.special_posts_idx = self.clean_HNJobPosts()
        post_data = self.create_posts_dict()

        return post_data

    def clean_HNJobPosts(self):
        # The posts which have no points, username, timestamp are special HNJobs posts so they 
        # dont have any comments or upvotes to track, they just point to another jonb post link
        # The count of elements in this string can filter out these special posts, normal posts
        # have 6 children elements, all others have less number of elements
        special_posts_idx = []
        for i, subtext_element in enumerate(self.tree.xpath('//tr[not(@id) and not(@class)]/td[@class="subtext"]')):
            if len(subtext_element.xpath('*')) < 6:
                special_posts_idx.append(i)
                del self.post_subtext[i*3]
                del self.post_subtext_links[i*3]
        return special_posts_idx

    def create_posts_dict(self):
        posts_list = list()
        post = dict()
        for i in range(len(self.post_string)-len(self.special_posts_idx)-1):
            if i not in self.special_posts_idx:
                post['title'] = self.post_string[i]
                post['story_url'] = self.post_url[i]
                post['timestamp'] = self.post_timestamp[i]
                post['points'] = self.post_points[i].split(' ')[0]
                post['username'] = self.post_subtext[i*3]
                post['comments'] = self.post_subtext[(i*3)+2].split('\xa0comments')[0]
                post['user_profile_url'] = f'https://news.ycombinator.com/{self.post_subtext_links[i*3]}'
                post['hn_post_url'] = f'https://news.ycombinator.com/{self.post_subtext_links[(i*3)+2]}'
                post['hn_id'] = post['hn_post_url'].split('=')[-1]
                self.scraped_hn_post_ids.append(int(post['hn_id']))
            posts_list.append(post.copy())
        return posts_list


# Unused logic to include HN posts instead of ignoring them
# def create_posts_with_hn_jobs(self):
    # i, end, change = 1, 30, 0
    # while(i <= end):
    #     # print(i-1, self.post_subtext[(start-1)*3 + change], (start-1)*3 + dataPosChange)
    #     post['title'] = self.post_string[i-1]
    #     post['story_url'] = self.post_url[i-1]
    #     post['points'] = self.post_url[i-1+change]
    #     post['timestamp'] = self.post_timestamp[i-1]
    #     post['username'] = self.post_subtext[(i-1)*3 + change].split('\xa0comments')[0]
    #     post['comments'] = self.post_subtext[(i-1)*2 + change + 2]
    #     post['user_profile_url'] =  f'https://news.ycombinator.com/{self.post_subtext[(i-1)*3 + change]}'
    #     post['hn_post_url'] = f'https://news.ycombinator.com/{self.post_subtext[(i-1)*2 + change + 2]}'

    #     if i in self.special_posts_idx:
    #         change += 1
    #         end -= change
    #         post['points'] = None
    #         post['username'] = None
    #         post['comments'] = None
    #         post['user_profile_url'] = None
    #         post['hn_post_url'] = None
    #     i += 1