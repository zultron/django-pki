# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CertificateAuthority'
        db.create_table('pki_certificateauthority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'pki', ['CertificateAuthority'])

        # Adding model 'Certificate'
        db.create_table('pki_certificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'pki', ['Certificate'])

        # Adding unique constraint on 'Certificate', fields ['name', 'parent']
        db.create_unique('pki_certificate', ['name', 'parent_id'])

        # Adding unique constraint on 'Certificate', fields ['common_name', 'parent']
        db.create_unique('pki_certificate', ['common_name', 'parent_id'])

        # Adding model 'PkiChangelog'
        db.create_table('pki_changelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_id', self.gf('django.db.models.fields.IntegerField')()),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'], null=True, blank=True)),
            ('changes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'pki', ['PkiChangelog'])

        # Adding model 'x509Extension'
        db.create_table('pki_x509extension', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'pki', ['x509Extension'])

        # Adding M2M table for field key_usage on 'x509Extension'
        db.create_table('pki_x509extension_key_usage', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('x509extension', models.ForeignKey(orm[u'pki.x509extension'], null=False)),
            ('keyusage', models.ForeignKey(orm[u'pki.keyusage'], null=False))
        ))
        db.create_unique('pki_x509extension_key_usage', ['x509extension_id', 'keyusage_id'])

        # Adding M2M table for field extended_key_usage on 'x509Extension'
        db.create_table('pki_x509extension_extended_key_usage', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('x509extension', models.ForeignKey(orm[u'pki.x509extension'], null=False)),
            ('extendedkeyusage', models.ForeignKey(orm[u'pki.extendedkeyusage'], null=False))
        ))
        db.create_unique('pki_x509extension_extended_key_usage', ['x509extension_id', 'extendedkeyusage_id'])

        # Adding model 'KeyUsage'
        db.create_table(u'pki_keyusage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'pki', ['KeyUsage'])

        # Adding model 'ExtendedKeyUsage'
        db.create_table(u'pki_extendedkeyusage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'pki', ['ExtendedKeyUsage'])


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
        db.delete_table(u'pki_keyusage')

        # Deleting model 'ExtendedKeyUsage'
        db.delete_table(u'pki_extendedkeyusage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pki.Certificate']", 'null': 'True', 'blank': 'True'}),
            'certificate_password': ('django_fields.fields.EncryptedCharField', [], {'default': "u''", 'max_length': '69', 'cipher': "'AES'", 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_employee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_ldap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ssn': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'pki.certificate': {
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
            'extension': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pki.x509Extension']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_length': ('django.db.models.fields.IntegerField', [], {'default': '1024'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pki.CertificateAuthority']", 'null': 'True', 'blank': 'True'}),
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
        u'pki.certificateauthority': {
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
            'extension': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pki.x509Extension']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_length': ('django.db.models.fields.IntegerField', [], {'default': '1024'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pki.CertificateAuthority']", 'null': 'True', 'blank': 'True'}),
            'parent_passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'passphrase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'policy': ('django.db.models.fields.CharField', [], {'default': "'policy_anything'", 'max_length': '50'}),
            'revoked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {})
        },
        u'pki.extendedkeyusage': {
            'Meta': {'object_name': 'ExtendedKeyUsage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'pki.keyusage': {
            'Meta': {'object_name': 'KeyUsage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'pki.pkichangelog': {
            'Meta': {'ordering': "['-action_time']", 'object_name': 'PkiChangelog', 'db_table': "'pki_changelog'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'changes': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_id': ('django.db.models.fields.IntegerField', [], {}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'})
        },
        u'pki.x509extension': {
            'Meta': {'object_name': 'x509Extension'},
            'authority_key_identifier': ('django.db.models.fields.CharField', [], {'default': "'keyid:always,issuer:always'", 'max_length': '255'}),
            'basic_constraints': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'basic_constraints_critical': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'crl_distribution_point': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'extended_key_usage': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pki.ExtendedKeyUsage']", 'null': 'True', 'blank': 'True'}),
            'extended_key_usage_critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_usage': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pki.KeyUsage']", 'symmetrical': 'False'}),
            'key_usage_critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'subject_key_identifier': ('django.db.models.fields.CharField', [], {'default': "'hash'", 'max_length': '255'})
        }
    }

    complete_apps = ['pki']