using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;

namespace plantchecker
{
    public partial class CreatePath : System.Web.UI.Page
    {
        int count = 0;
        protected void Page_Load(object sender, EventArgs e)
        {
          
        }

        protected void btnclickone_click(object sender, EventArgs e)
        {
            if (count == 0)
            {
                robot plantbot = new robot();
                string[] data = plantbot.readdata();

                landwidth.Value = data[0];

                //here I can make code to load what is currently in the text file so that it can be reused again when starting the robot path
                count = count + 1;
            }

        }

        protected void btnclick_click(object sender, EventArgs e)
        {
            String w = landwidth.Value;
            robot plantbot = new robot(w);
            plantbot.senddata();
        }
    }
}