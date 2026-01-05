# StudyDeck Forum
A simple reddit-like platform written in DJango.

## Setup Instructions

Clone the repository
```
git clone https://github.com/VarMonke/studydeck_forum.git
```
Create a venv for your project
```
python -m venv .venv
source .venv/bin/activate on Linux
(or)
.venv\Scripts\activate.bat for Windows
pip install -r requirements.txt

```

Go to `impartus_app/example_settings.py` and rename it to `impartus_app/settings.py` and enter your `"client_id"` and `"secret"` under `SOCIALACCOUNT_PROVIDERS`. Make sure these URLs are valid, and your `Google Cloud Console` is setup with the URLs for your website.

You can run a local instance by
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Head over to http://localhost:8000/ to see the website.

Head over to http://localhost:8000/admin to create your Moderator and Student roles and assign all the `Forum` permissions to the Moderator.

To populate the database(with test data), run
```
python manage.py populate_data
```


# Feature Walkthrough
## BITS Pilani Email only login
Subclassing `DefaultSocialAccountAdapter` allows us to restrict login to only `pilani.bits-pilani.ac.in`.
## Assigning Moderator Roles
Due to nature of `DJango Admin`, assigning users Moderator permissions is relatively simple.
## Threads
- Admins can create `Categories` and `Tags` which allow users to sort threads depending on these factors.
- Users can include `Resources` which they are reffering to, in the post as well.
- Users can Upvote and Downvote threads and comments.
- Pagination is available on the `Thread List` and `Comments`.

- Moderators and Admins can view reports at `base_url.com/moderation/reports/` and resolve them.
## Moderation
- Users can report threads and comments.
- Moderators and Admin can lock threads and delete comments.
- Deleted comments are soft deleted, i.e the content is not visible to the user but still available in the database.
- Moderators and Admins can view reports at `base_url.com/moderation/reports/` and resolve them.
- Reports highlight the specific reply reported.