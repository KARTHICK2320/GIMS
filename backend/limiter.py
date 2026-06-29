from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure rate limiter using client IP address
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]  # Applied selectively to specific endpoints via decorators
)

