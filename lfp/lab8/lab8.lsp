;; Лабораторна робота №8 (Lisp)
;; Функції планування, лямбда-вирази, замикання

(format t "=== Lab work #8 (Lisp) ===~%")

;; Приклад 1: mapcar з лямбда
(let ((numbers '(1 2 3 4 5)))
  (format t "Squares: ~A~%" 
          (mapcar (lambda (x) (* x x)) numbers)))

;; Приклад 2: reduce з лямбда
(let ((numbers '(1 2 3 4 5)))
  (format t "Sum: ~A~%" 
          (reduce (lambda (x y) (+ x y)) numbers)))

;; Приклад 3: лексичне замикання
(defun make-counter ()
  (let ((count 0))
    (lambda ()
      (incf count)
      count)))

(let ((counter (make-counter)))
  (format t "Counter: ~A ~A ~A~%" 
          (funcall counter) (funcall counter) (funcall counter)))
