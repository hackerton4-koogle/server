from django.core.management.base import BaseCommand

from Restaurants.models import Category, Food
from translation.models import Language, Original, Romanization, Translation

import pandas as pd

class Command(BaseCommand):
    help = 'Initialize languages, translations'

    def init_languages(self):
        languages = pd.read_csv('languages.csv')

        for _, row in languages.iterrows():
            Language.objects.update_or_create(
                name=row['name'],
                defaults={'code': row['code']},
            )
    

    def init_translations(self):
        translation = pd.read_csv('translation_presets.csv')

        supported_languages = Language.objects.values_list('name', flat=True).exclude(name='한국어')
        korean, _ = Language.objects.get_or_create(name='한국어')

        translation_languages = translation.columns.tolist()

        for _, row in translation.iterrows():
            original_instance, _ = Original.objects.get_or_create(
                language=korean,
                text=row['한국어']
            )
            for lang in translation_languages:
                if lang in supported_languages:
                    lang_instance = Language.objects.get(name=lang)
                    
                    if pd.notnull(row[lang]):
                        Translation.objects.update_or_create(
                            language=lang_instance, 
                            original=original_instance, 
                            defaults={'translated': row[lang]},
                        )
        
                if pd.notnull(row['로마자화']):
                    Romanization.objects.update_or_create(
                        original=original_instance,
                        defaults={'romanized': row['로마자화']}
                    )
        

    def handle(self, *args, **options):
        self.init_languages()
        self.stdout.write(self.style.SUCCESS('Supported languages initialized'))

        self.init_translations()
        self.stdout.write(self.style.SUCCESS('Translation preset initialized'))

        return 0