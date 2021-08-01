from django.db import models


class CrawlRun(models.Model):
    '''
    Represents a single run for the crawler, the posts that will be fetched 
    or updated for this run will get their Foreign Keys updated to point to the
    latest run that has the freshest data.

    Attributes:
        id: UUID primary key
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    posts_created = models.IntegerField(default=0)
    posts_updated = models.IntegerField(default=0)

class Post(models.Model):
    '''
    Represents a hackernews post, all the metadata scraped from HN will
    be saved in this model.

    Attributes:
        id: Primary key, same as HN unique post ID
        title: Post title
        story_url: URL for story linked to the post
        timestamp: time posted
        points: Upvotes that the post got
        comments: Number of comments for the post
        posted_by: Username of the poster
        poster_profile_url: URL to poster's HN profile
        hn_post_url: HackerNews URL for the post
        crawl_run: FK pointing to the last run the data was article was updated on
    '''
    id = models.PositiveBigIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    story_url = models.URLField()
    timestamp = models.DateTimeField()
    points = models.IntegerField()
    comments = models.CharField(max_length=50)
    posted_by = models.CharField(max_length=200)
    poster_profile_url = models.URLField()
    hn_post_url = models.URLField()
    crawl_run = models.ForeignKey(
        CrawlRun,
        db_index=False, 
        on_delete=models.CASCADE
    )


