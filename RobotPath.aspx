<%@ Page Language="C#" AutoEventWireup="true" MasterPageFile="~/Site.Master" CodeBehind="RobotPath.aspx.cs" Inherits="plantchecker.CreatePath" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
<body>
        
        <div class="form-floating mb-3">
            <input type="text" class="form-control" id="landwidth" placeholder="in metres" runat="server">
            <label for="floatingInput">Width of Row(m)</label>
        </div>
        <asp:Button ID="Button2" CssClass="btn btn-success mb-3" runat="server" onclick="btnclickone_click" Text="Fill Previous Path" />
        <div></div>
        <asp:Button ID="Button1" CssClass="btn btn-success mb-3" runat="server" onclick="btnclick_click" Text="Start Path" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
</body>
</asp:Content>
