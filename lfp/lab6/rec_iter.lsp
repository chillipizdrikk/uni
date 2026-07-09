;;; Завдання 1
;;; Перевірка, чи список складається лише з дробових чисел

(defun in-interval-rec (lst a b)
  (cond
    ((null lst) t)
    ((and (numberp (car lst))
          (floatp (car lst))
          (>= (car lst) a)
          (<= (car lst) b))
     (in-interval-rec (cdr lst) a b))
    (t nil)))

(defun in-interval-iter (lst a b)
  (let ((ok t))
    (dolist (x lst ok)
      (unless (and (numberp x)
                   (floatp x)
                   (>= x a)
                   (<= x b))
        (setf ok nil)))))

;;; Приклади:
;; (in-interval-rec '(1.2 2.5 3.0) 1.0 3.5) ; => T
;; (in-interval-iter '(1.2 5.0 2.1) 1.0 3.5) ; => NIL


;;; Завдання 2
;;; Для кожної групи з m елементів поруч обчислити суму

(defun group-sums-rec (lst m)
  (if (null lst)
      nil
      (cons (apply #'+ (subseq lst 0 m))
            (group-sums-rec (nthcdr m lst) m))))

(defun group-sums-iter (lst m)
  (let ((result '()))
    (loop for i from 0 below (length lst) by m do
      (push (apply #'+ (subseq lst i (min (+ i m) (length lst)))) result))
    (nreverse result)))

;;; Приклади:
;; (group-sums-rec '(1 2 3 4 5 6) 2) ; => (3 7 11)
;; (group-sums-iter '(1 2 3 4 5 6 7 8) 3) ; => (6 15 15)


;;; Завдання 3
;;; Для кожного підсписку: розвернути та додати суму

(defun reverse-with-sum-rec (lst)
  (if (null lst)
      nil
      (let* ((sub (car lst))
             (rev (reverse sub))
             (sum (apply #'+ sub)))
        (cons (append rev (list sum))
              (reverse-with-sum-rec (cdr lst))))))

(defun reverse-with-sum-iter (lst)
  (let ((result '()))
    (dolist (sub lst (nreverse result))
      (push (append (reverse sub) (list (apply #'+ sub))) result))))

;;; Приклади:
;; (reverse-with-sum-rec '((1 2 3) (4 5))) ; => ((3 2 1 6) (5 4 9))
;; (reverse-with-sum-iter '((2 2 2) (1 1 1 1))) ; => ((2 2 2 6) (1 1 1 1 4))

(format t "~%Test 1 (in-interval-rec): ~A"
        (in-interval-rec '(1.2 5.0 2.1) 1.0 3.5))

(format t "~%Test 2 (group-sums-rec): ~A"
        (group-sums-rec '(1 2 3 4 5 6) 2))

(format t "~%Test 3 (reverse-with-sum-rec): ~A"
        (reverse-with-sum-iter '((2 2 4) (1 1 2 1))))
        
