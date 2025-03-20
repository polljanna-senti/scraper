import os


class ArticlePipeline:
    def process_item(self, item, spider):
        # Tworzenie katalogu na artykuły
        os.makedirs("articles", exist_ok=True)

        # Przygotowanie bezpiecznej nazwy pliku
        safe_title = "".join(c if c.isalnum() or c.isspace() else "_" for c in item['title'])[:50].strip()
        file_path = f"articles/{safe_title}.md"

        # Zapis artykułu w formacie Markdown
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(item['markdown'])

        return item
