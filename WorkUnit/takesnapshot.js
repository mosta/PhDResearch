var casper = require('casper').create();
 
casper.start(casper.cli.get(0), function() {    
    this.echo(this.getHTML());
    var t = casper.cli.get(1);
    this.capture("Snapshots/"+t+".png") 
});
casper.run();

