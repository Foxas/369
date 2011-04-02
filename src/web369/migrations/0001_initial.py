# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BaseWord'
        db.create_table('web369_baseword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('stop_word', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web369', ['BaseWord'])

        # Adding model 'Word'
        db.create_table('web369_word', (
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True, db_index=True)),
            ('base', self.gf('django.db.models.fields.related.ForeignKey')(related_name='derivatives', to=orm['web369.BaseWord'])),
        ))
        db.send_create_signal('web369', ['Word'])

        # Adding model 'ScrappedDocument'
        db.create_table('web369_scrappeddocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.IntegerField')()),
            ('crawl_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('crawl_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('crawl_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('item_id', self.gf('django.db.models.fields.IntegerField')()),
            ('item_link', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_ascii', self.gf('django.db.models.fields.TextField')()),
            ('content_length', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('content_word_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('subject_title', self.gf('django.db.models.fields.CharField')(max_length=555, null=True)),
            ('subject_title_ascii', self.gf('django.db.models.fields.CharField')(max_length=555, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subject_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('web369', ['ScrappedDocument'])


    def backwards(self, orm):
        
        # Deleting model 'BaseWord'
        db.delete_table('web369_baseword')

        # Deleting model 'Word'
        db.delete_table('web369_word')

        # Deleting model 'ScrappedDocument'
        db.delete_table('web369_scrappeddocument')


    models = {
        'web369.baseword': {
            'Meta': {'object_name': 'BaseWord'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop_word': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'web369.scrappeddocument': {
            'Meta': {'object_name': 'ScrappedDocument'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_ascii': ('django.db.models.fields.TextField', [], {}),
            'content_length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'content_word_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'crawl_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'crawl_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'document_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.IntegerField', [], {}),
            'item_link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.IntegerField', [], {}),
            'subject_id': ('django.db.models.fields.IntegerField', [], {}),
            'subject_title': ('django.db.models.fields.CharField', [], {'max_length': '555', 'null': 'True'}),
            'subject_title_ascii': ('django.db.models.fields.CharField', [], {'max_length': '555', 'null': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'web369.word': {
            'Meta': {'object_name': 'Word'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derivatives'", 'to': "orm['web369.BaseWord']"}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['web369']
