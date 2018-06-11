const {exec } = require('child_process');
var module_pat = /Error: Cannot find module '(.*)'/g
function trial_install(cmd,maxi_trials) {
    for (i =0 ; i < maxi_trials; i++){
        exec('node bin/www',(err,stdout,stderr) =>{
                if(err ) {
                   console.log(`stderr:${stderr}`);
                   if (matches = module_pat.exec(stderr)) {
                       console.log(matches[1])
                       module_name = matches[1]
                       exec(`npm install ${module_name}  --save`,(err,stdout,stderr)=>{
                            if(err ) {
                               console.log(`stderr:${stderr}`);
                            } else {
                               console.log(`stdout:${stdout}`);
                            }

                       })
                   }

                   i +=1;
                } else {
                   console.log(`stdout:${stdout}`);
                   console.log(`stderr:${stderr}`);
                   return  
                }
       })
    }
}

trial_install('node bin/wwww',7)

