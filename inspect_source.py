import zipfile, xml.etree.ElementTree as E
p = r"C:\Users\hp\Downloads\InsightForge_AI_Prompt_Engineering_Methodology.pptx"
z = zipfile.ZipFile(p)
ns = {"a":"http://schemas.openxmlformats.org/drawingml/2006/main","p":"http://schemas.openxmlformats.org/presentationml/2006/main"}
print("size", E.fromstring(z.read("ppt/presentation.xml")).find("p:sldSz",ns).attrib)
for n in [2,3,10]:
    r = E.fromstring(z.read(f"ppt/slides/slide{n}.xml"))
    print("SLIDE",n)
    for sp in r.findall(".//p:sp",ns):
        meta=sp.find("./p:nvSpPr/p:cNvPr",ns); xfrm=sp.find("./p:spPr/a:xfrm",ns)
        o=xfrm.find("a:off",ns) if xfrm is not None else None
        ex=xfrm.find("a:ext",ns) if xfrm is not None else None
        txt=" / ".join(t.text or "" for t in sp.findall(".//a:t",ns))
        print(meta.get("id"),meta.get("name"),(o.attrib if o is not None else ""),(ex.attrib if ex is not None else ""),txt[:180])
