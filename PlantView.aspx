<%@ Page Language="C#" AutoEventWireup="true" MasterPageFile="~/Site.Master" CodeBehind="PlantView.aspx.cs" Inherits="plantchecker.PlantView" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
<body>
        <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">General Map of Current Plant Row</label>
            <textarea class="form-control" id="generalmaptextarea" rows="3" runat="server"></textarea>
        </div>
        <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">Disease Map of Current Plant Row</label>
            <textarea class="form-control" id="diseasemaptextarea" rows="3" runat="server"></textarea>
        </div>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
</body>
</asp:Content>
