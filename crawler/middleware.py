import logging
from proxy import PROXIES
from agents import AGENTS

import random

class CustomHttpProxyMiddleware(object):
    logger = logging.getLogger('Proxy')
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            # print '==PROXY==' * 5
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                logger.info("Exception %s" % e, _level=log.CRITICAL)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        # return False
        return True
        # if "depth" in request.meta and int(request.meta['depth']) <= 2:
        #     return False
        # i = random.randint(1, 10)
        # return i <= 6


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        # print '==Agent==' * 10
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
