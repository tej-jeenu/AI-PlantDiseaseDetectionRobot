using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.IO;
using System.Web.UI.WebControls;

namespace plantchecker
{
    public class robot
    { 
        
        private double forwardincrements;
        private String detailsfilepath = @"C:\Users\jeenu\Desktop\python programs\PlantCheckerProject\pathdetails.txt";
        private String commandfilepath = @"C:\Users\jeenu\Desktop\python programs\PlantCheckerProject\command.txt";
        public robot(String landwidth)
        {
      //distance between plants is the same is the small increment the bot moves to scan them//each pattern covers 2 rows therefore the repeats of the pattern is the rownum over 2
            forwardincrements = double.Parse(landwidth) / 0.5;
        }

        public robot()
        {
            //for general purpose usage
        }

        public void senddata()
        {
            File.Delete(detailsfilepath);
            //File.Delete(commandfilepath);
            //this method will write details to a specific file
            string[] line = {
               forwardincrements.ToString(),
            };

            string[] line2 = {
               "PATH",
            };

            File.WriteAllLines(detailsfilepath, line);
            File.WriteAllLines(commandfilepath, line2);
            
        }

        public string[] readdata()
        {
            string[] data = File.ReadAllLines(detailsfilepath);
            
            String landwidth = (double.Parse(data[0]) * 0.5).ToString();
           
            string[] datanew = {landwidth};
            return datanew;    
        }
        
    }
}