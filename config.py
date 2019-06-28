import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RESULTS_PER_API_CALL = 25

    @staticmethod
    def init_app(app):
        """
        If some configuration needs to initialize the app in some way use this function
        :param app: Flask app
        :return:
        """
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hunter02"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'default': DevelopmentConfig
}
