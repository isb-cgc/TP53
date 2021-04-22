// Fonction crŽŽe fncourreil(ARG)
// user: name of the person; host: domain name; cuser: name of the person (CC); chost: domaine name 
// sbj: subject; tag: text which appears with the link. If blank, the complete address appears as the link  

function fncouriel(user,host,cuser,chost,sbj,tag) { 
                                       eml= "<a href=mailto:" + user +"@" + host;
                                       if ((cuser!=="")||(sbj!=="")) eml=eml + "?";
                                       if (cuser!=="") eml=eml + "CC=" + cuser + "@" + chost;
                                       if ((cuser!=="")&&(sbj!=="")) eml=eml + "&";
                                       if (sbj!=="") eml=eml + "Subject=" + sbj;
                                       eml=eml + ">";
                                       (tag=="")? eml=eml + user +"@" + host: eml=eml + " " + tag;
                                       eml=eml + "</a>";
                                       document.write(eml);
                                       }
                                       
                                       
function fncouriel2(user,cuser,chost,sbj,tag) { // Pour definir une adresse electronique d'une personne du CIRC  
									   var host = "iarc.fr";
                                       eml= "<a href=mailto:" + user +"@" + host;
                                       if ((cuser!=="")||(sbj!=="")) eml=eml + "?";
                                       if (cuser!=="") eml=eml + "CC=" + cuser + "@" + chost;
                                       if ((cuser!=="")&&(sbj!=="")) eml=eml + "&";
                                       if (sbj!=="") eml=eml + "Subject=" + sbj;
                                       eml=eml + ">";
                                       (tag=="")? eml=eml + user +"@" + host: eml=eml + " " + tag;
                                       eml=eml + "</a>";
                                       document.write(eml);
                                       }
//***********************************************************************
// Pour definir une adresse electronique d'une personne du CIRC                                       
function fncouriel3(user,tag) { 
			 var host = "iarc.fr";
             eml= "<a href=mailto:" + user +"@" + host;
             eml=eml + ">";
             (tag=="")? eml=eml + user +"@" + host: eml=eml + " " + tag;
             eml=eml + "</a>";
             document.write(eml);
             }  

//EXAMPLE JAVASCRIPT code to set a link to GEP Group email address
//	<script language="JavaScript" type="text/javascript">fncouriel3('gep','');</script>
													
													
//***********************************************************************
// Pour definir une adresse electronique d'une personne externe             
function fncouriel3b(user,host,tag) { 
                                       eml= "<a href=mailto:" + user +"@" + host;
                                       eml=eml + ">";
                                       (tag=="")? eml=eml + user +"@" + host: eml=eml + " " + tag;
                                       eml=eml + "</a>";
                                       document.write(eml);
                                       }

//EXAMPLE JAVASCRIPT code to set a link to m.willson@mwcommunications.org.uk
//<script language="JavaScript" type="text/javascript">fncouriel3b('m.willson','mwcommunications.org.uk','');</script>



//***********************************************************************


// Pour definir une adresse electronique sur une image                                       
function fncourielimg(user,host) { 
								   var host2 = "iarc.fr";
								   eml= "<a href=mailto:" + user +"@";
                                   (host=="")? eml=eml + host2: eml=eml + host;
                                   eml=eml + ">";
                                   document.write(eml);
                                 }
