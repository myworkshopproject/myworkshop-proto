# Generated by Django 3.1.7 on 2021-04-21 21:23

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import publications.models.image
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('id', models.CharField(editable=False, max_length=6, primary_key=True, serialize=False)),
                ('source', models.TextField(blank=True, help_text='You can use Markdown syntax.', verbose_name='source')),
                ('toc', models.TextField(blank=True, editable=False)),
                ('html', models.TextField(blank=True, editable=False)),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='publications_publications_as_owner', related_query_name='publications_publication_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'publication',
                'verbose_name_plural': 'publications',
                'ordering': ['-changed_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publications.publication')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publications.publication')),
                ('picture', models.ImageField(storage=publications.models.image.OverwriteStorage(), upload_to=publications.models.image.image_path, verbose_name='picture')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publications.publication')),
            ],
            options={
                'verbose_name': 'tutorial',
                'verbose_name_plural': 'tutorials',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='HistoricalTutorial',
            fields=[
                ('publication_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='publications.publication')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('id', models.CharField(db_index=True, editable=False, max_length=6)),
                ('source', models.TextField(blank=True, help_text='You can use Markdown syntax.', verbose_name='source')),
                ('toc', models.TextField(blank=True, editable=False)),
                ('html', models.TextField(blank=True, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='publications_publication_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical tutorial',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPublication',
            fields=[
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('id', models.CharField(db_index=True, editable=False, max_length=6)),
                ('source', models.TextField(blank=True, help_text='You can use Markdown syntax.', verbose_name='source')),
                ('toc', models.TextField(blank=True, editable=False)),
                ('html', models.TextField(blank=True, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='publications_publication_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical publication',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalImage',
            fields=[
                ('publication_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='publications.publication')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('id', models.CharField(db_index=True, editable=False, max_length=6)),
                ('source', models.TextField(blank=True, help_text='You can use Markdown syntax.', verbose_name='source')),
                ('toc', models.TextField(blank=True, editable=False)),
                ('html', models.TextField(blank=True, editable=False)),
                ('picture', models.CharField(max_length=100, verbose_name='picture')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='publications_publication_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical image',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalArticle',
            fields=[
                ('publication_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='publications.publication')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('id', models.CharField(db_index=True, editable=False, max_length=6)),
                ('source', models.TextField(blank=True, help_text='You can use Markdown syntax.', verbose_name='source')),
                ('toc', models.TextField(blank=True, editable=False)),
                ('html', models.TextField(blank=True, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='publications_publication_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical article',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
