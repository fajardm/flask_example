from app.domain.blacklist_token.model import BlacklistToken


def create(token):
    blacklisted = BlacklistToken(token)
    blacklisted.save()
    return blacklisted
