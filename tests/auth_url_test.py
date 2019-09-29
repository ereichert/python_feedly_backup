import json


# TODO Move to its own module
# TODO Add methods for reading the creds from files.
class GoogleCredentials:

    def __init__(self, client_id, auth_uri, redirect_uris):
        self.client_id = client_id
        self.auth_uri = auth_uri
        self.redirect_uris = redirect_uris


# TODO Added tests for missing keys
def parse_google_credentials(credentials):
    parsed_json = json.loads(credentials)
    installed = parsed_json['installed']
    return GoogleCredentials(
        installed['client_id'],
        installed['auth_uri'],
        installed['redirect_uris'],
    )


# TODO Move to its own module
# TODO Add methods for reading the configs from files.
class FeedlyBackupConfig:

    def __init__(self, response_type, scope):
        self.response_type = response_type
        self.scope = scope


# TODO Added tests for missing keys
def parse_feedly_backup_config(config):
    parsed_json = json.loads(config)
    return FeedlyBackupConfig(
        parsed_json['google_auth_response_type'],
        parsed_json['google_api_scope'],
    )


# TODO Move to its own module
def generate_auth_url(google_creds, backup_config):
    return (f'{google_creds.auth_uri}?'
            f'scope={backup_config.scope}'
            f'&redirect_uri={google_creds.redirect_uris[0]}'
            f'&response_type={backup_config.response_type}'
            f'&client_id={google_creds.client_id}')


RAW_TEST_CREDENTIALS = ('{"installed": {'
                        '"client_id": "client_id.apps.googleusercontent.com",'
                        '"project_id": "pythonfeedlybackup",'
                        '"auth_uri": "https://accounts.google.com/o/oauth2/auth",'
                        '"token_uri": "https://oauth2.googleapis.com/token",'
                        '"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",'
                        '"client_secret": "very secret client",'
                        '"redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]'
                        '}}')

RAW_TEST_CONFIG = ('{'
                   '"google_auth_response_type": "code",'
                   '"google_api_scope": "https://www.googleapis.com/auth/gmail.readonly"'
                   '}')


# TODO Move the tests to their proper locations
def test_parse_feedly_backup_config_returns_the_config_with_scope():
    config = parse_feedly_backup_config(RAW_TEST_CONFIG)

    assert config.scope == 'https://www.googleapis.com/auth/gmail.readonly'


def test_parse_feedly_backup_config_returns_the_config_with_response_type():
    config = parse_feedly_backup_config(RAW_TEST_CONFIG)

    assert config.response_type == 'code'


def test_parse_google_credentials_returns_google_credentials_with_redirect_uri():
    credentials = parse_google_credentials(RAW_TEST_CREDENTIALS)

    assert credentials.redirect_uris == ['urn:ietf:wg:oauth:2.0:oob', 'http://localhost']


def test_parse_google_credentials_returns_google_credentials_with_auth_uri():
    credentials = parse_google_credentials(RAW_TEST_CREDENTIALS)

    assert credentials.auth_uri == 'https://accounts.google.com/o/oauth2/auth'


def test_parse_google_credentials_returns_google_credentials_with_client_id():
    credentials = parse_google_credentials(RAW_TEST_CREDENTIALS)

    assert credentials.client_id == 'client_id.apps.googleusercontent.com'


def test_generate_auth_url_produces_correct_url():
    test_config = parse_feedly_backup_config(RAW_TEST_CONFIG)
    test_creds = parse_google_credentials(RAW_TEST_CREDENTIALS)
    auth_url = generate_auth_url(test_creds, test_config)

    assert auth_url == ('https://accounts.google.com/o/oauth2/auth?'
                        'scope=https://www.googleapis.com/auth/gmail.readonly'
                        '&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
                        '&response_type=code'
                        '&client_id=client_id.apps.googleusercontent.com')
