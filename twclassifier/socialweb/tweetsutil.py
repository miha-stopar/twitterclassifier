import sys  
import time
from datetime import datetime
from urllib2 import URLError
import twitter

def exec_twitter_request(t, twitter_function, max_errors=3, *args, **kwargs): 
    wait_period = 2
    error_count = 0
    while True:
        try:
            return twitter_function(*args, **kwargs)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = _handle_twitter_http_error(e, t, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except Exception, e:
            # todo
            print >> sys.stderr, str(e)
            
def _handle_twitter_http_error(e, t, wait_period=2):
    if wait_period > 3600: # Seconds
        print >> sys.stderr, 'Too many retries. Quitting.'
        raise e
    if e.e.code == 400:
        #todo: fix this
        print >> sys.stderr, 'Bad status request.'
        _wait(t)
        return 2
    elif e.e.code == 401:
        print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
        return None
    elif e.e.code in (502, 503):
        print >> sys.stderr, 'Encountered %i Error. Will retry in %i seconds' % (e.e.code,
                wait_period)
        time.sleep(wait_period)
        wait_period *= 1.5
        return wait_period
    elif _get_remaining_hits(t) == 0:
        _wait(t)
        return 2
    else:
        raise e
    
def _wait(t):
    status = t.account.rate_limit_status()
    now = time.time()  # UTC
    print >> sys.stdout, "now: %s" % datetime.now()
    when_rate_limit_resets = status['reset_time_in_seconds']  # UTC
    sleep_time = max(when_rate_limit_resets - now, 5) # Prevent negative numbers
    print >> sys.stderr, 'Rate limit reached: sleeping for %i secs' % (sleep_time, )
    time.sleep(sleep_time)
    
def _get_remaining_hits(t):
    return t.account.rate_limit_status()['remaining_hits']

