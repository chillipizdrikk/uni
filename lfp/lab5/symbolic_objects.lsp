(defun put (symbol property value)
  (setf (get symbol property) value))

;;; Define symbolic persons
(put 'ME 'name "Marta")
(put 'ME 'age 20)
(put 'ME 'occupation "student")
(put 'ME 'skills '(programming math modeling))
(put 'ME 'interests '(simulations AI forest-fires))

(put 'FRIEND 'name "Iryna")
(put 'FRIEND 'age 22)
(put 'FRIEND 'occupation "researcher")
(put 'FRIEND 'skills '(math data-analysis modeling))
(put 'FRIEND 'interests '(ecology travel simulations))

;;; Access property
(defun get-property (symbol property)
  (get symbol property))

;;; Print full info
(defun print-info (symbol)
  (format t "~%Info about ~A:" symbol)
  (format t "~%Name: ~A" (get symbol 'name))
  (format t "~%Age: ~A" (get symbol 'age))
  (format t "~%Occupation: ~A" (get symbol 'occupation))
  (format t "~%Skills: ~A" (get symbol 'skills))
  (format t "~%Interests: ~A~%" (get symbol 'interests)))

;;; Set or update property
(defun set-property (symbol property value)
  (put symbol property value))

;;; Compare ages using EQL
(defun compare-age-eql (sym1 sym2)
  (let ((age1 (get sym1 'age))
        (age2 (get sym2 'age)))
    (cond ((eql age1 age2) 'equal)
          ((> age1 age2) sym1)
          (t sym2))))

;;; Find common skills using intersection
(defun common-skills (sym1 sym2)
  (let ((skills1 (get sym1 'skills))
        (skills2 (get sym2 'skills)))
    (intersection skills1 skills2)))

;;; Add new skill using CONS
(defun add-skill (symbol new-skill)
  (let ((skills (get symbol 'skills)))
    (put symbol 'skills (cons new-skill skills))))

;;; Show first skill using CAR
(defun first-skill (symbol)
  (car (get symbol 'skills)))

;;; Show rest of skills using CDR
(defun rest-skills (symbol)
  (cdr (get symbol 'skills)))

;;; Check if name is atom using ATOM
(defun is-name-atom (symbol)
  (atom (get symbol 'name)))

;;; Demonstration
(print-info 'ME)
(print-info 'FRIEND)

(format t "~%Who is older: ~A~%" (compare-age-eql 'ME 'FRIEND))
(format t "~%Common skills: ~A~%" (common-skills 'ME 'FRIEND))

(add-skill 'ME 'lisp)
(format t "~%Added skill 'lisp' to ME. New skills: ~A~%" (get 'ME 'skills))

(format t "~%First skill of FRIEND: ~A~%" (first-skill 'FRIEND))
(format t "~%Rest of FRIEND's skills: ~A~%" (rest-skills 'FRIEND))

(format t "~%Is ME's name atomic? ~A~%" (is-name-atom 'ME))





; (print (get 'ME 'skills))
; (print (cdr (get 'ME 'skills)))

