import os
from Cython import Tempita


def render_templates(pxifiles):
    for pxifile in pxifiles:
        # build pxifiles first, template extension must be *.in
        outfile = pxifile[:-3]

        if (
            os.path.exists(outfile)
            and os.stat(pxifile).st_mtime < os.stat(outfile).st_mtime
        ):
            # if .pxi.in is not updated, no need to output .pxi
            continue

        with open(pxifile) as f:
            tmpl = f.read()
        pyxcontent = Tempita.sub(tmpl)

        with open(outfile, "w") as f:
            f.write(pyxcontent)

if __name__ == '__main__':
    import sys
    lst= sys.argv[1::]
    render_templates(lst)

