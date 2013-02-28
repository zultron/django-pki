# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CertificateAuthority'
        db.create_table('pki_certificateauthority', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(default='DE', max_length=2)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('OU', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('valid_days', self.gf('django.db.models.fields.IntegerField')()),
            ('key_length', self.gf('django.db.models.fields.IntegerField')(default=1024)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('revoked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('ca_chain', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('der_encoded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action', self.gf('django.db.models.fields.CharField')(default='create', max_length=32)),
            ('extension', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pki.x509Extension'], null=True, blank=True)),
            ('crl_dpoints', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pki.CertificateAuthority'], null=True, blank=True)),
            ('passphrase', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('parent_passphrase', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('policy', self.gf('django.db.models.fields.CharField')(default='policy_anything', max_length=50)),
        ))
        db.send_create_signal('pki', ['CertificateAuthority'])

        # Adding model 'Certificate'
        db.create_table('pki_certificate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(default='DE', max_length=2)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('OU', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('valid_days', self.gf('django.db.models.fields.IntegerField')()),
            ('key_length', self.gf('django.db.models.fields.IntegerField')(default=1024)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('revoked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('ca_chain', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('der_encoded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action', self.gf('django.db.models.fields.CharField')(default='create', max_length=32)),
            ('extension', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pki.x509Extension'], null=True, blank=True)),
            ('crl_dpoints', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pki.CertificateAuthority'], null=True, blank=True)),
            ('passphrase', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent_passphrase', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pkcs12_encoded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pkcs12_passphrase', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subjaltname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('pki', ['Certificate'])

        # Adding unique constraint on 'Certificate', fields ['name', 'parent']
        db.create_unique('pki_certificate', ['name', 'parent_id'])

        # Adding unique constraint on 'Certificate', fields ['common_name', 'parent']
        db.create_unique('pki_certificate', ['common_name', 'parent_id'])

        # Adding model 'PkiChangelog'
        db.create_table('pki_changelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_id', self.gf('django.db.models.fields.IntegerField')()),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[settings.AUTH_USER_MODEL], null=True, blank=True)),
            ('changes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('pki', ['PkiChangelog'])

        # Adding model 'x509Extension'
        db.create_table('pki_x509extension', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('basic_constraints', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('basic_constraints_critical', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('key_usage_critical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extended_key_usage_critical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subject_key_identifier', self.gf('django.db.models.fields.CharField')(default='hash', max_length=255)),
            ('authority_key_identifier', self.gf('django.db.models.fields.CharField')(default='keyid:always,issuer:always', max_length=255)),
            ('crl_distribution_point', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pki', ['x509Extension'])

        # Adding M2M table for field key_usage on 'x509Extension'
        db.create_table('pki_x509extension_key_usage', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('x509extension', models.ForeignKey(orm['pki.x509extension'], null=False)),
            ('keyusage', models.ForeignKey(orm['pki.keyusage'], null=False))
        ))
        db.create_unique('pki_x509extension_key_usage', ['x509extension_id', 'keyusage_id'])

        # Adding M2M table for field extended_key_usage on 'x509Extension'
        db.create_table('pki_x509extension_extended_key_usage', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('x509extension', models.ForeignKey(orm['pki.x509extension'], null=False)),
            ('extendedkeyusage', models.ForeignKey(orm['pki.extendedkeyusage'], null=False))
        ))
        db.create_unique('pki_x509extension_extended_key_usage', ['x509extension_id', 'extendedkeyusage_id'])

        # Adding model 'KeyUsage'
        db.create_table('pki_keyusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('pki', ['KeyUsage'])

        # Adding model 'ExtendedKeyUsage'
        db.create_table('pki_extendedkeyusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('pki', ['ExtendedKeyUsage'])


    def backwards(self, orm):
        # Removing unique constraint on 'Certificate', fields ['common_name', 'parent']
        db.delete_unique('pki_certificate', ['common_name', 'parent_id'])

        # Removing unique constraint on 'Certificate', fields ['name', 'parent']
        db.delete_unique('pki_certificate', ['name', 'parent_id'])

        # Deleting model 'CertificateAuthority'
        db.delete_table('pki_certificateauthority')

        # Deleting model 'Certificate'
        db.delete_table('pki_certificate')

        # Deleting model 'PkiChangelog'
        db.delete_table('pki_changelog')

        # Deleting model 'x509Extension'
        db.delete_table('pki_x509extension')

        # Removing M2M table for field key_usage on 'x509Extension'
        db.delete_table('pki_x509extension_key_usage')

        # Removing M2M table for field extended_key_usage on 'x509Extension'
        db.delete_table('pki_x509extension_extended_key_usage')

        # Deleting model 'KeyUsage'
        db.delete_table('pki_keyusage')

        # Deleting model 'ExtendedKeyUsage'
        db.delete_table('pki_extendedkeyusage')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pki.certificate': {
            'Meta': {'unique_together': "(('name', 'parent'), ('common_name', 'parent'))", 'object_name': 'Certificate'},
            'OU': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'create'", 'max_length': '32'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ca_chain': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'DE'", 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'crl_dpoints': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'der_encoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'extension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pki.x509Extension']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_length': ('django.db.models.fields.IntegerField', [], {'default': '1024'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pki.CertificateAuthority']", 'null': 'True', 'blank': 'True'}),
            'parent_passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pkcs12_encoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pkcs12_passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'revoked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'subjaltname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {})
        },
        'pki.certificateauthority': {
            'Meta': {'object_name': 'CertificateAuthority'},
            'OU': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'create'", 'max_length': '32'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ca_chain': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'DE'", 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'crl_dpoints': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'der_encoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'extension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pki.x509Extension']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_length': ('django.db.models.fields.IntegerField', [], {'default': '1024'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pki.CertificateAuthority']", 'null': 'True', 'blank': 'True'}),
            'parent_passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'policy': ('django.db.models.fields.CharField', [], {'default': "'policy_anything'", 'max_length': '50'}),
            'revoked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {})
        },
        'pki.extendedkeyusage': {
            'Meta': {'object_name': 'ExtendedKeyUsage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'pki.keyusage': {
            'Meta': {'object_name': 'KeyUsage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'pki.pkichangelog': {
            'Meta': {'ordering': "['-action_time']", 'object_name': 'PkiChangelog', 'db_table': "'pki_changelog'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'changes': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_id': ('django.db.models.fields.IntegerField', [], {}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'pki.x509extension': {
            'Meta': {'object_name': 'x509Extension'},
            'authority_key_identifier': ('django.db.models.fields.CharField', [], {'default': "'keyid:always,issuer:always'", 'max_length': '255'}),
            'basic_constraints': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'basic_constraints_critical': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'crl_distribution_point': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'extended_key_usage': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pki.ExtendedKeyUsage']", 'null': 'True', 'blank': 'True'}),
            'extended_key_usage_critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_usage': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pki.KeyUsage']", 'symmetrical': 'False'}),
            'key_usage_critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'subject_key_identifier': ('django.db.models.fields.CharField', [], {'default': "'hash'", 'max_length': '255'})
        }
    }

    complete_apps = ['pki']