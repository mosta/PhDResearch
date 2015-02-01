var casper = require('casper').create();
 
casper.start(casper.cli.get(0), function() {    
    this.echo(this.getHTML());
    var path = casper.cli.get(1);
    var t = casper.cli.get(2);
    this.capture(path+t+".png") 
});
casper.run();

