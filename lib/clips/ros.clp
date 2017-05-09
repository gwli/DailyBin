(defrule how-to-navigating-TheFileSystem ""
   ("I know roscd")
  =>
  (printout t "adfadf" crlf))


(defclass compoent_interface (is-a OBJECT)
    (slot add)
    (slot delete)
    (slot edit)
    (slot save)
    (slot load)
    (slot get-set-dump)
    (slot search)
)

(assert (cd  roscd)
        (dpkg  rospack)
        (apt-get rosstack)
        (ls   rosls)
        (exec roscall)
        (service rossrv)
        (console rqt)
        (editor  rosed)
        (make    rosmake)
        (msg     rosmsg)
        (faq     roswtf)  
)

