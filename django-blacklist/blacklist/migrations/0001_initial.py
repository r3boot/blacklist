# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ConfigStore'
        db.create_table('blacklist_configstore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('blacklist', ['ConfigStore'])

        # Adding model 'Country'
        db.create_table('blacklist_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('additional', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whitelisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blacklist', ['Country'])

        # Adding model 'Duration'
        db.create_table('blacklist_duration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
        ))
        db.send_create_signal('blacklist', ['Duration'])

        # Adding model 'Key'
        db.create_table('blacklist_key', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, db_index=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('blacklist', ['Key'])

        # Adding model 'Role'
        db.create_table('blacklist_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, db_index=True)),
            ('view', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rpc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blacklist', ['Role'])

        # Adding model 'RIR'
        db.create_table('blacklist_rir', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, db_index=True)),
            ('whois', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whitelisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_providers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_subnets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_listed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_whitelisted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_history', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('blacklist', ['RIR'])

        # Adding model 'ASNum'
        db.create_table('blacklist_asnum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asnum', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Country'])),
            ('rir', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.RIR'])),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')()),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whitelisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_subnets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_listed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_whitelisted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_history', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('blacklist', ['ASNum'])

        # Adding model 'Subnet'
        db.create_table('blacklist_subnet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subnet', self.gf('django.db.models.fields.DecimalField')(max_digits=39, decimal_places=0, db_index=True)),
            ('mask', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('last', self.gf('django.db.models.fields.DecimalField')(max_digits=39, decimal_places=0, db_index=True)),
            ('asnum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.ASNum'], null=True, blank=True)),
            ('af', self.gf('django.db.models.fields.IntegerField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Country'])),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')()),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whitelisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_listed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_whitelisted', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('blacklist', ['Subnet'])

        # Adding model 'IP'
        db.create_table('blacklist_ip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.DecimalField')(max_digits=39, decimal_places=0, db_index=True)),
            ('mask', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('last', self.gf('django.db.models.fields.DecimalField')(max_digits=39, decimal_places=0, db_index=True)),
            ('subnet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Subnet'], null=True, blank=True)),
            ('af', self.gf('django.db.models.fields.IntegerField')()),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whitelisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_listed', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('blacklist', ['IP'])

        # Adding model 'Host'
        db.create_table('blacklist_host', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, db_index=True)),
            ('ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.IP'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('blacklist', ['Host'])

        # Adding model 'Sensor'
        db.create_table('blacklist_sensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, db_index=True)),
        ))
        db.send_create_signal('blacklist', ['Sensor'])

        # Adding model 'Peering'
        db.create_table('blacklist_peering', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('peer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Host'])),
            ('asnum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.ASNum'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Key'])),
        ))
        db.send_create_signal('blacklist', ['Peering'])

        # Adding model 'Reason'
        db.create_table('blacklist_reason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Sensor'])),
        ))
        db.send_create_signal('blacklist', ['Reason'])

        # Adding model 'Rule'
        db.create_table('blacklist_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.TextField')()),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Sensor'])),
            ('pos_ip', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_reason', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('blacklist', ['Rule'])

        # Adding model 'Ignore'
        db.create_table('blacklist_ignore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ignore', self.gf('django.db.models.fields.TextField')()),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Sensor'])),
        ))
        db.send_create_signal('blacklist', ['Ignore'])

        # Adding model 'Listing'
        db.create_table('blacklist_listing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.IP'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Reason'])),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Sensor'])),
            ('sensor_host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Host'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Duration'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('blacklist', ['Listing'])

        # Adding model 'HistoryListing'
        db.create_table('blacklist_historylisting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.IP'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Reason'])),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Sensor'])),
            ('sensor_host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Host'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.Duration'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('blacklist', ['HistoryListing'])

        # Adding model 'WhiteListing'
        db.create_table('blacklist_whitelisting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blacklist.IP'])),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('blacklist', ['WhiteListing'])


    def backwards(self, orm):
        
        # Deleting model 'ConfigStore'
        db.delete_table('blacklist_configstore')

        # Deleting model 'Country'
        db.delete_table('blacklist_country')

        # Deleting model 'Duration'
        db.delete_table('blacklist_duration')

        # Deleting model 'Key'
        db.delete_table('blacklist_key')

        # Deleting model 'Role'
        db.delete_table('blacklist_role')

        # Deleting model 'RIR'
        db.delete_table('blacklist_rir')

        # Deleting model 'ASNum'
        db.delete_table('blacklist_asnum')

        # Deleting model 'Subnet'
        db.delete_table('blacklist_subnet')

        # Deleting model 'IP'
        db.delete_table('blacklist_ip')

        # Deleting model 'Host'
        db.delete_table('blacklist_host')

        # Deleting model 'Sensor'
        db.delete_table('blacklist_sensor')

        # Deleting model 'Peering'
        db.delete_table('blacklist_peering')

        # Deleting model 'Reason'
        db.delete_table('blacklist_reason')

        # Deleting model 'Rule'
        db.delete_table('blacklist_rule')

        # Deleting model 'Ignore'
        db.delete_table('blacklist_ignore')

        # Deleting model 'Listing'
        db.delete_table('blacklist_listing')

        # Deleting model 'HistoryListing'
        db.delete_table('blacklist_historylisting')

        # Deleting model 'WhiteListing'
        db.delete_table('blacklist_whitelisting')


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
        'blacklist.asnum': {
            'Meta': {'object_name': 'ASNum'},
            'asnum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'num_history': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_listed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_subnets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_whitelisted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {}),
            'rir': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.RIR']"}),
            'whitelisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'blacklist.configstore': {
            'Meta': {'object_name': 'ConfigStore'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'blacklist.country': {
            'Meta': {'ordering': "['code']", 'object_name': 'Country'},
            'additional': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'whitelisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'blacklist.duration': {
            'Meta': {'object_name': 'Duration'},
            'duration': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'blacklist.historylisting': {
            'Meta': {'object_name': 'HistoryListing'},
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Duration']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.IP']"}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Reason']"}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Sensor']"}),
            'sensor_host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Host']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'blacklist.host': {
            'Meta': {'object_name': 'Host'},
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.IP']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'blacklist.ignore': {
            'Meta': {'object_name': 'Ignore'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.TextField', [], {}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Sensor']"})
        },
        'blacklist.ip': {
            'Meta': {'object_name': 'IP'},
            'af': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.DecimalField', [], {'max_digits': '39', 'decimal_places': '0', 'db_index': 'True'}),
            'last': ('django.db.models.fields.DecimalField', [], {'max_digits': '39', 'decimal_places': '0', 'db_index': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mask': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'num_listed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subnet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Subnet']", 'null': 'True', 'blank': 'True'}),
            'whitelisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'blacklist.key': {
            'Meta': {'object_name': 'Key'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'})
        },
        'blacklist.listing': {
            'Meta': {'object_name': 'Listing'},
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Duration']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.IP']"}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Reason']"}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Sensor']"}),
            'sensor_host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Host']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'blacklist.peering': {
            'Meta': {'object_name': 'Peering'},
            'asnum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.ASNum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Key']"}),
            'peer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Host']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'blacklist.reason': {
            'Meta': {'object_name': 'Reason'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Sensor']"})
        },
        'blacklist.rir': {
            'Meta': {'object_name': 'RIR'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'num_history': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_listed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_providers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_subnets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_whitelisted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'whitelisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'whois': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'blacklist.role': {
            'Meta': {'object_name': 'Role'},
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'rpc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'view': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'blacklist.rule': {
            'Meta': {'object_name': 'Rule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos_ip': ('django.db.models.fields.IntegerField', [], {}),
            'pos_reason': ('django.db.models.fields.IntegerField', [], {}),
            'rule': ('django.db.models.fields.TextField', [], {}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Sensor']"})
        },
        'blacklist.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'})
        },
        'blacklist.subnet': {
            'Meta': {'object_name': 'Subnet'},
            'af': ('django.db.models.fields.IntegerField', [], {}),
            'asnum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.ASNum']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.DecimalField', [], {'max_digits': '39', 'decimal_places': '0', 'db_index': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mask': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'num_listed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_whitelisted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {}),
            'subnet': ('django.db.models.fields.DecimalField', [], {'max_digits': '39', 'decimal_places': '0', 'db_index': 'True'}),
            'whitelisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'blacklist.whitelisting': {
            'Meta': {'object_name': 'WhiteListing'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blacklist.IP']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blacklist']
