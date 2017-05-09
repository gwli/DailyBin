
(defrule tracking-use-IUM ""
   (IMU ?)
   (OGL transform-matrix)
   =>
   (printout t " use IMU data as transform-matrix" crlf)
)




(assert (data-set http://projects.asl.ethz.ch/datasets/doku.php?id=home))
(assert (IMU Interinal_measurement_unit))
(assert (OGL transform-matrix))
