using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.IO;

namespace plantchecker
{
    public class Farmer
    {
        private String firstname = "";
        private String lastname = "";
        private String phonenumber = "";
        private String keywords = "";
        private String commandfilepath = @"C:\Users\jeenu\Desktop\python programs\PlantCheckerProject\command.txt";

        public Farmer(String f, String l, String p, String k)
        {
            firstname = f;
            lastname = l;
            phonenumber = p;
            keywords = k;
        }

        public Farmer(String f, String l)
        {
            firstname = f;
            lastname = l;
        }

        public void add()
        {
            //File.Delete(commandfilepath);
            string lines = "ADD" + "-" + firstname + " " + lastname + "-" + phonenumber + "-(" + keywords + ")";
            File.WriteAllText(commandfilepath, lines);
        }

        public void remove()
        {
            //File.Delete(commandfilepath);
            string lines = "REMOVE" + "-" + firstname + " " + lastname;
            File.WriteAllText(commandfilepath, lines);
        }
    }
}