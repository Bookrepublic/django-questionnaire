# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Questionnaire'
        db.create_table('questionnaire_questionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
        ))
        db.send_create_signal('questionnaire', ['Questionnaire'])

        # Adding model 'QuestionSet'
        db.create_table('questionnaire_questionset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Questionnaire'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('questionnaire', ['QuestionSet'])

        # Adding model 'Question'
        db.create_table('questionnaire_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionSet'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('questionnaire', ['Question'])

        # Adding model 'Choice'
        db.create_table('questionnaire_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Question'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('questionnaire', ['Choice'])


    def backwards(self, orm):
        # Deleting model 'Questionnaire'
        db.delete_table('questionnaire_questionnaire')

        # Deleting model 'QuestionSet'
        db.delete_table('questionnaire_questionset')

        # Deleting model 'Question'
        db.delete_table('questionnaire_question')

        # Deleting model 'Choice'
        db.delete_table('questionnaire_choice')


    models = {
        'questionnaire.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionSet']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'})
        },
        'questionnaire.questionset': {
            'Meta': {'object_name': 'QuestionSet'},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']"})
        }
    }

    complete_apps = ['questionnaire']