import uno
import unohelper
from com.enigmacurry.SpotMetal import XSpotMetal
import urllib2
import time

class SpotMetalImpl( unohelper.Base, XSpotMetal ):
    def __init__( self, ctx ):
        self.ctx = ctx
        self.data = None
        self.last_grab = 0
    def spotMetal(self, metal, bidAsk):
        if (time.time() - self.last_grab) > 300:
            self.spotMetalRefresh()
        else:
            print("Retrieving cached spot price...")
        if metal.lower() == "gold":
            return self.data[0][bidAsk]
        if metal.lower() == "silver":
            return self.data[1][bidAsk]
    def spotMetalRefresh(self):
        print("Refreshing spot prices..")
        self.data = eval(urllib2.urlopen("http://chartseeker.com/quotes/metals.txt").read())
        print("Done.")
        self.last_grab = time.time()
        
                
def createInstance( ctx ):
    return SpotMetalImpl( ctx )
    
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.enigmacurry.SpotMetal.python.SpotMetalImpl",
    ("com.sun.star.sheet.AddIn",),)
