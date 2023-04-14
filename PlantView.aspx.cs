using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;

namespace plantchecker
{
    public partial class PlantView : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            String generalmapfilepath = @"C:\Users\jeenu\Desktop\python programs\PlantCheckerProject\generalmap.txt";
            String diseasemapfilepath = @"C:\Users\jeenu\Desktop\python programs\PlantCheckerProject\diseasemap.txt";

            String generalmap = "";
            String diseasemap = "";

            string[] generalmaprows = File.ReadAllLines(generalmapfilepath);
            string[] diseasemaprows = File.ReadAllLines(diseasemapfilepath);

            foreach (String line in generalmaprows)
            {
                generalmap = generalmap + line + Environment.NewLine;
            }

            diseasemap = diseasemaprows[0] + Environment.NewLine + diseasemaprows[1];

            generalmaptextarea.Value = generalmap;
            diseasemaptextarea.Value = diseasemap;
        }
        
    }
}