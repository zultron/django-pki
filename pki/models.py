from django.db import models
from logging import getLogger
from shutil import rmtree

from pki.openssl import handle_exception, OpensslActions, OpensslCaManagement, md5_constructor, refresh_pki_metadata
from pki.settings import ADMIN_MEDIA_PREFIX 

import datetime

logger = getLogger("pki")

##------------------------------------------------------------------##
## Choices
##------------------------------------------------------------------##

KEY_LENGTH = ( (1024, '1024'), (2048, '2048'), (4096, '4096'), )
POLICY     = ( ('policy_match', 'policy_match'), ('policy_anything', 'policy_anything'), )
ACTIONS    = ( ('create', 'create'), ('update', 'update'), ('revoke', 'revoke'), ('renew', 'renew'), )
CA_TYPES   = ( ('RootCA', 'self-signed (RootCA)'), ('SubCA', 'SubCA'), )
EXTENSIONS = ( ('v3_server_cert', 'V3 Server'), ('v3_client_cert', 'V3 Client' ), )
COUNTRY    = ( ('AD', 'AD'),('AE', 'AE'),('AF', 'AF'),('AG', 'AG'),('AI', 'AI'),('AL', 'AL'),('AM', 'AM'),
               ('AN', 'AN'),('AO', 'AO'),('AQ', 'AQ'),('AR', 'AR'),('AS', 'AS'),('AT', 'AT'),('AU', 'AU'),
               ('AW', 'AW'),('AZ', 'AZ'),('BA', 'BA'),('BB', 'BB'),('BD', 'BD'),('BE', 'BE'),('BF', 'BF'),
               ('BG', 'BG'),('BH', 'BH'),('BI', 'BI'),('BJ', 'BJ'),('BM', 'BM'),('BN', 'BN'),('BO', 'BO'),
               ('BR', 'BR'),('BS', 'BS'),('BT', 'BT'),('BU', 'BU'),('BV', 'BV'),('BW', 'BW'),('BY', 'BY'),
               ('BZ', 'BZ'),('CA', 'CA'),('CC', 'CC'),('CF', 'CF'),('CG', 'CG'),('CH', 'CH'),('CI', 'CI'),
               ('CK', 'CK'),('CL', 'CL'),('CM', 'CM'),('CN', 'CN'),('CO', 'CO'),('CR', 'CR'),('CS', 'CS'),
               ('CU', 'CU'),('CV', 'CV'),('CX', 'CX'),('CY', 'CY'),('CZ', 'CZ'),('DD', 'DD'),('DE', 'DE'),
               ('DJ', 'DJ'),('DK', 'DK'),('DM', 'DM'),('DO', 'DO'),('DZ', 'DZ'),('EC', 'EC'),('EE', 'EE'),
               ('EG', 'EG'),('EH', 'EH'),('ER', 'ER'),('ES', 'ES'),('ET', 'ET'),('FI', 'FI'),('FJ', 'FJ'),
               ('FK', 'FK'),('FM', 'FM'),('FO', 'FO'),('FR', 'FR'),('FX', 'FX'),('GA', 'GA'),('GB', 'GB'),
               ('GD', 'GD'),('GE', 'GE'),('GF', 'GF'),('GH', 'GH'),('GI', 'GI'),('GL', 'GL'),('GM', 'GM'),
               ('GN', 'GN'),('GP', 'GP'),('GQ', 'GQ'),('GR', 'GR'),('GS', 'GS'),('GT', 'GT'),('GU', 'GU'),
               ('GW', 'GW'),('GY', 'GY'),('HK', 'HK'),('HM', 'HM'),('HN', 'HN'),('HR', 'HR'),('HT', 'HT'),
               ('HU', 'HU'),('ID', 'ID'),('IE', 'IE'),('IL', 'IL'),('IN', 'IN'),('IO', 'IO'),('IQ', 'IQ'),
               ('IR', 'IR'),('IS', 'IS'),('IT', 'IT'),('JM', 'JM'),('JO', 'JO'),('JP', 'JP'),('KE', 'KE'),
               ('KG', 'KG'),('KH', 'KH'),('KI', 'KI'),('KM', 'KM'),('KN', 'KN'),('KP', 'KP'),('KR', 'KR'),
               ('KW', 'KW'),('KY', 'KY'),('KZ', 'KZ'),('LA', 'LA'),('LB', 'LB'),('LC', 'LC'),('LI', 'LI'),
               ('LK', 'LK'),('LR', 'LR'),('LS', 'LS'),('LT', 'LT'),('LU', 'LU'),('LV', 'LV'),('LY', 'LY'),
               ('MA', 'MA'),('MC', 'MC'),('MD', 'MD'),('MG', 'MG'),('MH', 'MH'),('ML', 'ML'),('MM', 'MM'),
               ('MN', 'MN'),('MO', 'MO'),('MP', 'MP'),('MQ', 'MQ'),('MR', 'MR'),('MS', 'MS'),('MT', 'MT'),
               ('MU', 'MU'),('MV', 'MV'),('MW', 'MW'),('MX', 'MX'),('MY', 'MY'),('MZ', 'MZ'),('NA', 'NA'),
               ('NC', 'NC'),('NE', 'NE'),('NF', 'NF'),('NG', 'NG'),('NI', 'NI'),('NL', 'NL'),('NO', 'NO'),
               ('NP', 'NP'),('NR', 'NR'),('NT', 'NT'),('NU', 'NU'),('NZ', 'NZ'),('OM', 'OM'),('PA', 'PA'),
               ('PE', 'PE'),('PF', 'PF'),('PG', 'PG'),('PH', 'PH'),('PK', 'PK'),('PL', 'PL'),('PM', 'PM'),
               ('PN', 'PN'),('PR', 'PR'),('PT', 'PT'),('PW', 'PW'),('PY', 'PY'),('QA', 'QA'),('RE', 'RE'),
               ('RO', 'RO'),('RU', 'RU'),('RW', 'RW'),('SA', 'SA'),('SB', 'SB'),('SC', 'SC'),('SD', 'SD'),
               ('SE', 'SE'),('SG', 'SG'),('SH', 'SH'),('SI', 'SI'),('SJ', 'SJ'),('SK', 'SK'),('SL', 'SL'),
               ('SM', 'SM'),('SN', 'SN'),('SO', 'SO'),('SR', 'SR'),('ST', 'ST'),('SU', 'SU'),('SV', 'SV'),
               ('SY', 'SY'),('SZ', 'SZ'),('TC', 'TC'),('TD', 'TD'),('TF', 'TF'),('TG', 'TG'),('TH', 'TH'),
               ('TJ', 'TJ'),('TK', 'TK'),('TM', 'TM'),('TN', 'TN'),('TO', 'TO'),('TP', 'TP'),('TR', 'TR'),
               ('TT', 'TT'),('TV', 'TV'),('TW', 'TW'),('TZ', 'TZ'),('UA', 'UA'),('UG', 'UG'),('UM', 'UM'),
               ('US', 'US'),('UY', 'UY'),('UZ', 'UZ'),('VA', 'VA'),('VC', 'VC'),('VE', 'VE'),('VG', 'VG'),
               ('VI', 'VI'),('VN', 'VN'),('VU', 'VU'),('WF', 'WF'),('WS', 'WS'),('YD', 'YD'),('YE', 'YE'),
               ('YT', 'YT'),('YU', 'YU'),('ZA', 'ZA'),('ZM', 'ZM'),('ZR', 'ZR'),('ZW', 'ZW'),('ZZ', 'ZZ'),
               ('ZZ', 'ZZ'),
              )

##------------------------------------------------------------------##
## Base DB classes
##------------------------------------------------------------------##

class CertificateBase(models.Model):
    '''Base class for all type of certificates'''
    
    common_name  = models.CharField(max_length=64, unique=True)
    name         = models.CharField(max_length=64, unique=True, help_text="Only change the suggestion if you really know what you're doing")
    description  = models.CharField(max_length=255)
    country      = models.CharField(max_length=2, choices=COUNTRY, default='DE')
    state        = models.CharField(max_length=32)
    locality     = models.CharField(max_length=32)
    organization = models.CharField(max_length=64)
    OU           = models.CharField(max_length=64,blank=True, null=True)
    email        = models.EmailField(blank=True, null=True)
    valid_days   = models.IntegerField()
    key_length   = models.IntegerField(choices=KEY_LENGTH, default=2048)
    expiry_date  = models.DateField(blank=True,null=True)
    created      = models.DateTimeField(blank=True,null=True)
    revoked      = models.DateTimeField(blank=True,null=True)
    active       = models.BooleanField(default=True, help_text="Turn off to revoke this certificate")
    serial       = models.CharField(max_length=64, blank=True, null=True)
    ca_chain     = models.CharField(max_length=200, blank=True, null=True)
    pem_encoded  = models.BooleanField(default=False)
    der_encoded  = models.BooleanField(default=False, verbose_name="Create DER encoded certificate (additional)")
    action       = models.CharField(max_length=32, choices=ACTIONS, default='create', help_text="Be careful: Revoking/renewing a self-signed \
                                    CA certificate will result in a completely broken chain!<br>Yellow fields can/have to be modified!")
    
    class Meta:
        abstract = True
    
    def get_icon_html(self, state):
        if state is True:
            return '<center><img src="%simg/admin/icon-yes.gif" alt="True" /></center>' % ADMIN_MEDIA_PREFIX
        else:
            return '<center><img src="%simg/admin/icon-no.gif" alt="False" /></center>'  % ADMIN_MEDIA_PREFIX

##------------------------------------------------------------------##
## Certificate authority class
##------------------------------------------------------------------##

class CertificateAuthority(CertificateBase):
    '''CA specification'''
    
    ##---------------------------------##
    ## Model definition
    ##---------------------------------##
    
    subcas_allowed    = models.BooleanField(verbose_name="Sub CA's allowed", help_text="If enabled you cannot sign certificates with this CA")
    parent            = models.ForeignKey('self', blank=True, null=True)
    type              = models.CharField(max_length=32, null=True, choices=CA_TYPES, default='RootCA')
    passphrase        = models.CharField(max_length=255, blank=True, help_text="At least 8 characters. Remeber this passphrase - <font color='red'> \
                                                                    <strong>IT'S NOT RECOVERABLE</strong></font><br>Will be shown as md5 encrypted string")
    parent_passphrase = models.CharField(max_length=255, null=True, blank=True, help_text="Leave empty if this is a top-level CA")
    pf_encrypted      = models.NullBooleanField()
    policy            = models.CharField(max_length=50, choices=POLICY, default='policy_anything', help_text='policy_match: All subject settings must \
                                                                                                              match the signing CA<br> \
                                                                                                              policy_anything: Nothing has to match the \
                                                                                                              signing CA')

    class Meta:
        verbose_name_plural = 'Certificate Authorities'
        permissions         = ( ( "can_download", "Can download certificate authority", ),
                                ( "can_revoke", "Can revoke certificate authority", ), )
    
    ##---------------------------------##
    ## Redefined functions
    ##---------------------------------##
    
    def save(self, force_insert=False, force_update=False):
        
        if self.pk:
            ### existing CA
            if self.action in ('update', 'revoke', 'renew'):
                
                action = OpensslActions('ca', self)
                prev   = CertificateAuthority.objects.get(pk=self.pk)
                
                if self.action == 'update':
                    
                    ## Create or remove DER certificate
                    if self.der_encoded:
                        action.generate_der_encoded()
                    else:
                        action.remove_der_encoded()
                    
                    prev.description = self.description
                    prev.der_encoded = self.der_encoded
                    
                elif self.action == 'revoke':
                    
                    ## Revoke and generate CRL
                    action.revoke_certificate(self.parent_passphrase)
                    action.generate_crl(self.parent.name, self.parent_passphrase)
                    
                    ## Modify fields
                    prev.parent_passphrase = None
                    prev.active            = False
                    prev.der_encoded       = False
                    prev.pem_encoded       = False
                    prev.revoked = datetime.datetime.now()
                    
                elif self.action == 'renew':
                    
                    ## Revoke if certificate is active
                    if self.active:
                        action.revoke_certificate(self.parent_passphrase)
                    
                    ## Rebuild the ca metadata
                    self.rebuild_ca_metadata(modify=True, task='replace')
                    
                    ## Renew and update CRL
                    action.renew_certificate()
                    action.generate_crl(self.parent.name, self.parent_passphrase)
                    
                    ## Modify fields
                    prev.created = datetime.datetime.now()
                    delta = datetime.timedelta(self.valid_days)
                    prev.expiry_date = datetime.datetime.now() + delta
                    
                    prev.parent_passphrase = None
                    prev.active            = True
                    prev.pem_encoded       = True
                    prev.der_encoded       = self.der_encoded
                    prev.revoked           = None
                    prev.subcas_allowed    = self.subcas_allowed
                    
                    ## Get the new serial
                    prev.serial     = action.get_serial_from_cert()
                    prev.passphrase = md5_constructor(self.passphrase).hexdigest()
                
                ## Save the data
                self = prev
                self.action = 'update'
                
                super(CertificateAuthority, self).save()
            else:
                
                handle_exception(handle_exception("%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name), \
                                                             'Invalid action %s supplied' % self.action, None))
        else:
            ## Set creation data
            self.created = datetime.datetime.now()
            delta = datetime.timedelta(self.valid_days)
            self.expiry_date = datetime.datetime.now() + delta
            
            ## Force instance to be active
            self.active = True
            
            ## Reset the action
            self.action = 'update'
            
            ## Rebuild the ca metadata
            self.rebuild_ca_metadata(modify=True, task='append')
            
            ## Generate keys and certificates
            action = OpensslActions('ca', self)
            action.generate_key()
            
            if not self.parent:
                action.generate_self_signed_cert()
            else:
                action.generate_csr()
                action.sign_csr()
            
            if self.der_encoded:
                action.generate_der_encoded()
            
            ## Generate CRL
            action.generate_crl(self.name, self.passphrase)
            
            ## Always enable pem encoded flag
            self.pem_encoded = True
            
            ## Get the serial from certificate
            self.serial = action.get_serial_from_cert()
            
            ## Generate ca chain (db field and chain file)
            chain = []
            chain_str = ''
            
            p = self.parent
            
            if self.parent == None:
                chain.append('self-signed')
            else:
                chain.append( self.name )
                while p != None:
                    chain.append(p.name)
                    p = p.parent
                
            chain.reverse()
            
            ## Build chain string and file
            for i in chain:
                if chain_str == '':
                    chain_str += '%s' % i
                    
                    if i == 'self-signed':
                        action.update_ca_chain_file(ca=self.name, mode='create')
                    else:
                        action.update_ca_chain_file(ca=i, mode='create')
                else:
                    chain_str += '&rarr;%s' % i
                    action.update_ca_chain_file(ca=i, mode='append')
            
            self.ca_chain = chain_str
            
            ## Encrypt passphrase and blank parent's passphrase
            self.passphrase = md5_constructor(self.passphrase).hexdigest()
            self.parent_passphrase = None
            
        ## Save the data
        super(CertificateAuthority, self).save()
    
    def delete(self, passphrase):
        
        logger.info( "Certificate %s is going to be deleted" % self.name )
        
        ## Container for CA folders to delete
        self.remove_chain = []
        
        ## Is a revoke required?
        revoke_required = True
        
        ## Helper function for recusion
        def chain_recursion(r_id):
            
            ca = CertificateAuthority.objects.get(pk=r_id)
            self.remove_chain.append(ca.name)
            
            ## Search for related CA's
            child_cas = CertificateAuthority.objects.filter(parent=r_id)
            if child_cas:
                for ca in child_cas:
                    chain_recursion(ca.pk)
        
        if not self.parent:
            logger.info( "No revoking of certitifcates. %s is a toplevel CA" % self.name )
            revoke_required = False
        else:
            ## Collect child CA's and certificates
            chain_recursion(self.pk)
            logger.info( "Full chain is %s and pf is %s" % (self.remove_chain, self.passphrase))
        
        ## Remoke first ca in the chain
        if revoke_required:
            c_action = OpensslActions('ca', CertificateAuthority.objects.get(pk=self.pk))
            c_action.revoke_certificate(passphrase)
            c_action.generate_crl(ca=self.parent.name, pf=passphrase)
        
        ## Rebuild the ca metadata
        self.rebuild_ca_metadata(modify=True, task='exclude')
        
        ## Call the "real" delete function
        super(CertificateAuthority, self).delete()
    
    ##---------------------------------##
    ## Helper functions
    ##---------------------------------##
    
    def rebuild_ca_metadata(self, modify, task):
        '''Wrapper around refresh_pki_metadata. Following the DRY principle'''
        
        logger.info("Rebuilding CA store")
        
        if modify:
            if task == 'append':
                ## Get list of all defined CA's
                known_cas = list(CertificateAuthority.objects.all())
                known_cas.append(self)
            elif task == 'replace':
                known_cas = list(CertificateAuthority.objects.exclude(pk=self.pk))
                known_cas.append(self)
            elif task == 'exclude':
                known_cas = list(CertificateAuthority.objects.exclude(pk=self.pk))
        else:
            known_cas = list(CertificateAuthority.objects.all())
        
        ## Rebuild the CA store metadata
        refresh_pki_metadata(known_cas)
    
    ##---------------------------------##
    ## View functions
    ##---------------------------------##
    
    def __unicode__(self):
        return self.name
    
    def active_center(self):
        '''Overwrite the Booleanfield admin for admin's changelist'''
        
        return self.get_icon_html(self.active)
    
    active_center.allow_tags = True
    active_center.short_description = 'Active'
    active_center.admin_order_field = 'active'
    
    def download(self):
        
        if not self.active:        
            crl   = '<font color="grey">crl</font>'
            chain = '<font color="grey">chain</font>'
            pem   = '<font color="grey">pem</font>'
            der   = '<font color="grey">der</font>'
        else:
            crl   = '<a href="/pki/ca-download/%s/crl"><strong>crl</strong></a>' % self.name
            chain = '<a href="/pki/ca-download/%s/chain"><strong>chain</strong></a>' % self.name
            pem   = '<a href="/pki/ca-download/%s/pem"><strong>pem</strong></a>' % self.name
            der   = '<font color="grey">der</font>'
            
            if self.der_encoded:
                der = '<a href="/pki/ca-download/%s/der"><strong>der</strong></a>' % self.name
        
        return ' | '.join((pem, der, chain, crl))
    
    download.allow_tags = True
    
    def Expiry_date(self):
        now = datetime.datetime.now().date()        
        diff = self.expiry_date - now
        
        day_string = 'd'
        
        if diff.days < 30:
            return '<font color="red"><strong>%s (%sd)</strong></font>' % (self.expiry_date, diff.days)
        else:
            return '%s (%sd)' % (self.expiry_date, diff.days)
    
    Expiry_date.allow_tags = True
    Expiry_date.admin_order_field = 'expiry_date'
    
    def CA_chain(self):
        return "%s" % self.ca_chain
    
    CA_chain.allow_tags = True
    CA_chain.admin_order_field = 'ca_chain'
    
    def Description(self):
        
        if len(self.description) > 30:
            return "%s..." % self.description[:30]
        else:
            return "%s" % self.description
    
    Description.allow_tags = True
    Description.admin_order_field = 'description'

##------------------------------------------------------------------##
## Certificate class
##------------------------------------------------------------------##

class Certificate(CertificateBase):
    '''CA specification'''
    
    parent            = models.ForeignKey('CertificateAuthority', blank=True, null=True, help_text='Leave blank to only generate a KEY and CSR')
    passphrase        = models.CharField(max_length=255, null=True, blank=True)
    pf_encrypted      = models.NullBooleanField()
    parent_passphrase = models.CharField(max_length=255, blank=True, null=True)
    pkcs12_encoded    = models.BooleanField(default=False, verbose_name="Create #PKCS12 encoded certificate (additional)")
    pkcs12_passphrase = models.CharField(max_length=255, verbose_name="#PKCS12 passphrase", blank=True, null=True)
    cert_extension    = models.CharField(max_length=64, choices=EXTENSIONS, verbose_name="Purpose")
    subjaltname       = models.CharField(max_length=255, blank=True, null=True, verbose_name="SubjectAltName", help_text='Refer to openssl \
                                         documentation for details' )

    class Meta:
        verbose_name_plural = 'Certificates'
        permissions         = ( ( "can_download", "Can download certificate", ),
                                ( "can_revoke", "Can revoke certificate", ),)

    
    ##---------------------------------##
    ## Redefined functions
    ##---------------------------------##
    
    def save(self):
        
        if self.pk:
            
            if self.action in ('update', 'revoke', 'renew'):
                
                action = OpensslActions('cert', self)
                prev   = Certificate.objects.get(pk=self.pk)
                
                if self.action == 'update':
                    
                    ## Create or remove DER certificate
                    if self.der_encoded:
                        action.generate_der_encoded()
                    else:
                        action.remove_der_encoded()
                    
                    ## Create or remove PKCS12 certificate
                    if self.pkcs12_encoded:
                        action.generate_pkcs12_encoded()
                    else:
                        action.remove_pkcs12_encoded()
                    
                    if self.pkcs12_passphrase:
                        prev.pkcs12_passphrase = md5_constructor(self.pkcs12_passphrase).hexdigest()
                    
                    prev.description    = self.description
                    prev.der_encoded    = self.der_encoded
                    prev.pkcs12_encoded = self.pkcs12_encoded
                    prev.pem_encoded    = True
                    
                elif self.action == 'revoke':
                    
                    ## Revoke and generate CRL
                    action.revoke_certificate(self.parent_passphrase)
                    action.generate_crl(self.parent.name, self.parent_passphrase)
                    
                    ## Modify fields
                    prev.parent_passphrase = None
                    prev.active            = False
                    prev.der_encoded       = False
                    prev.pem_encoded       = False
                    prev.pkcs12_encoded    = False
                    prev.revoked = datetime.datetime.now()
                    
                elif self.action == 'renew':
                    
                    ## Revoke is certificate is active
                    if self.active:
                        action.revoke_certificate(self.parent_passphrase)
                    
                    ## Renew and update CRL
                    action.renew_certificate()
                    action.generate_crl(self.parent.name, self.parent_passphrase)
                    
                    ## Modify fields
                    prev.created = datetime.datetime.now()
                    delta = datetime.timedelta(self.valid_days)
                    prev.expiry_date = datetime.datetime.now() + delta
                    
                    prev.parent_passphrase = None
                    prev.active            = True
                    prev.pem_encoded       = True
                    prev.der_encoded       = self.der_encoded
                    prev.pkcs12_encoded    = self.pkcs12_encoded
                    prev.revoked           = None
                    
                    ## Get the new serial
                    prev.serial     = action.get_serial_from_cert()
                    prev.passphrase = md5_constructor(self.passphrase).hexdigest()
                
                ## Save the data
                self = prev
                self.action = 'update'
                
                super(Certificate, self).save()
        else:
            ## Set creation data
            self.created = datetime.datetime.now()
            delta = datetime.timedelta(self.valid_days)
            self.expiry_date = datetime.datetime.now() + delta
            
            ## Force instance to be active
            self.active = True
            
            logger.info( "***** { New certificate generation: %s } *****" % self.name )
            
            ## Generate key and certificate
            action = OpensslActions('cert', self)
            
            action.generate_key()
            action.generate_csr()
            action.sign_csr()
            
            ## Get the serial from certificate
            self.serial = action.get_serial_from_cert()
            
            self.ca_chain = self.parent.ca_chain
            
            self.pem_encoded = True
            
            ## Create or remove DER certificate
            if self.der_encoded:
                action.generate_der_encoded()
            else:
                action.remove_der_encoded()
            
            ## Create or remove PKCS12 certificate
            if self.pkcs12_encoded:
                action.generate_pkcs12_encoded()
            else:
                action.remove_pkcs12_encoded()
            
            if self.pkcs12_passphrase:
                self.pkcs12_passphrase = md5_constructor(self.pkcs12_passphrase).hexdigest()
            
            ## Encrypt passphrase and blank parent's passphrase
            if self.passphrase:
                self.passphrase = md5_constructor(self.passphrase).hexdigest()
            
            self.parent_passphrase = None
            
            ## Save the data
            super(Certificate, self).save()
    
    def delete(self, passphrase):
        
        logger.info( "Certificate %s is going to be deleted" % self.name )
        
        ## Remoke first ca in the chain
        c_action = OpensslActions('cert', Certificate.objects.get(pk=self.pk))
        c_action.revoke_certificate(passphrase)
        c_action.generate_crl(ca=self.parent.name, pf=passphrase)
        
        ## Time for some rm action
        a = OpensslActions('cert', self)
        a.remove_complete_certificate()
        
        ## Call the "real" delete function
        super(Certificate, self).delete()

    ##---------------------------------##
    ## View functions
    ##---------------------------------##
    
    def __unicode__(self):
        return self.name
    
    def Expiry_date(self):
        now = datetime.datetime.now().date()        
        diff = self.expiry_date - now
        
        day_string = 'days'
        
        if diff.days == 1:
            day_string = 'day'
            
        if diff.days < 30:
            return '<font color="red"><strong>%s (%s %s)</strong></font>' % (self.expiry_date, diff.days, day_string)
        else:
            return '%s (%s %s)' % (self.expiry_date, diff.days, day_string)
    
    Expiry_date.allow_tags = True
    
    def CA_chain(self):
        return "%s" % self.ca_chain
    
    CA_chain.allow_tags = True
    
    def active_center(self):
        '''Overwrite the Booleanfield admin for admin's changelist'''
        
        return self.get_icon_html(self.active)
    
    active_center.allow_tags = True
    active_center.short_description = 'Active'
    
    def pem_encoded_center(self):
        '''Overwrite the Booleanfield admin for admin's changelist'''
        
        return self.get_icon_html(self.pem_encoded)
    
    pem_encoded_center.allow_tags = True
    pem_encoded_center.short_description = 'PEM'
    
    def p12_encoded_center(self):
        '''Overwrite the Booleanfield admin for admin's changelist'''
        
        return self.get_icon_html(self.pkcs12_encoded)
    
    p12_encoded_center.allow_tags = True
    p12_encoded_center.short_description = 'P12'
    
    def der_encoded_center(self):
        '''Overwrite the Booleanfield admin for admin's changelist'''
        
        return self.get_icon_html(self.der_encoded)
    
    der_encoded_center.allow_tags = True
    der_encoded_center.short_description = 'DER'
    
    def actions(self):
        '''Define actions for admin's changelist'''
        
        return '<a href="/ca-manage/%d/revoke"<strong>revoke</strong></a> | <a href="/ca-manage/%d/renew"<strong>renew</strong></a>' % (self.id,self.id)
    
    actions.allow_tags = True
    
    def download(self):
        
        der   = '<font color="grey">der</font>'
        p12   = '<font color="grey">p12</font>'
        chain = '<font color="grey">chain</font>'
        pem   = '<font color="grey">pem</font>'
        csr   = '<font color="grey">csr</font>'
        key   = '<font color="grey">key</font>'
        
        if self.active:
            
            chain = '<a href="/pki/cert-download/%s/chain"><strong>chain</strong></a>' % self.name
            pem   = '<a href="/pki/cert-download/%s/pem"><strong>pem</strong></a>' % self.name
            key   = '<a href="/pki/cert-download/%s/key"><strong>key</strong></a>' % self.name
            csr   = '<a href="/pki/cert-download/%s/csr"><strong>csr</strong></a>' % self.name
            
            if self.der_encoded:
                der = '<a href="/pki/cert-download/%s/der"><strong>der</strong></a>' % self.name
            
            if self.pkcs12_encoded:
                p12 = '<a href="/pki/cert-download/%s/pkcs12"><strong>p12</strong></a>' % self.name
        
        return ' | '.join((key, csr, pem, der, p12, chain))
    
    download.allow_tags = True
    
    def Description(self):
        
        if len(self.description) > 30:
            return "%s..." % self.description[:30]
        else:
            return "%s" % self.description
    
    Description.allow_tags = True
    Description.admin_order_field = 'description'