from django.core.management.base import BaseCommand
from forum.models import Category, Tag, Course, Resource


class Command(BaseCommand):
    help = "Populate initial categories, tags, courses, and resources"

    def handle(self, *args, **options):

        categories = [
            "Academics",
            "Internships",
            "Placements",
            "Campus Life",
            "Resources",
        ]

        category_objs = {}
        for name in categories:
            obj, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower().replace(" ", "-")}
            )
            category_objs[name] = obj

        self.stdout.write(self.style.SUCCESS("Categories populated"))

        tags = [
            "help",
            "important",
            "exam",
            "assignment",
            "tips",
            "notes",
            "pyp",
        ]

        tag_objs = {}
        for name in tags:
            obj, _ = Tag.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower()}
            )
            tag_objs[name] = obj

        self.stdout.write(self.style.SUCCESS("Tags populated"))

        courses = [
            {
                "code": "CS F111",
                "title": "Computer Programming",
                "department": "Computer Science",
            },
            {
                "code": "MATH F101",
                "title": "Calculus",
                "department": "Mathematics",
            },
            {
                "code": "PHY F101",
                "title": "Physics",
                "department": "Physics",
            },
        ]

        course_objs = {}
        for c in courses:
            obj, _ = Course.objects.get_or_create(
                code=c["code"],
                defaults={
                    "title": c["title"],
                    "department": c["department"],
                }
            )
            course_objs[c["code"]] = obj

        self.stdout.write(self.style.SUCCESS("Courses populated"))

        resources = [
            # CS F111
            {
                "course": "CS F111",
                "title": "CS F111 Lecture Slides",
                "resource_type": "pdf",
                "link": "https://example.com/csf111/slides",
            },
            {
                "course": "CS F111",
                "title": "CS F111 Previous Year Papers",
                "resource_type": "pdf",
                "link": "https://example.com/csf111/pyp",
            },
            {
                "course": "CS F111",
                "title": "CS F111 Practice Problems",
                "resource_type": "link",
                "link": "https://example.com/csf111/problems",
            },

            # MATH F101
            {
                "course": "MATH F101",
                "title": "MATH F101 Lecture Notes",
                "resource_type": "pdf",
                "link": "https://example.com/mathf101/notes",
            },
            {
                "course": "MATH F101",
                "title": "MATH F101 Tutorial Sheets",
                "resource_type": "pdf",
                "link": "https://example.com/mathf101/tutorials",
            },
            {
                "course": "MATH F101",
                "title": "MATH F101 Previous Year Papers",
                "resource_type": "pdf",
                "link": "https://example.com/mathf101/pyp",
            },
        ]

        for r in resources:
            Resource.objects.get_or_create(
                course=course_objs[r["course"]],
                title=r["title"],
                resource_type=r["resource_type"],
                link=r["link"],
            )

        self.stdout.write(self.style.SUCCESS("Resources populated"))

        self.stdout.write(self.style.SUCCESS("🎉 Database population complete"))
