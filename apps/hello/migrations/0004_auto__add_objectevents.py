# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ObjectEvents'
        db.create_table(u'hello_objectevents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('object_model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('object_repr', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'hello', ['ObjectEvents'])


    def backwards(self, orm):
        # Deleting model 'ObjectEvents'
        db.delete_table(u'hello_objectevents')


    models = {
        u'hello.appuser': {
            'Meta': {'object_name': 'AppUser'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hello.objectevents': {
            'Meta': {'object_name': 'ObjectEvents'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_repr': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hello.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['hello']