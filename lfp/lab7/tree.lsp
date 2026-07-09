;; -------------------------------
;; Лабораторна робота №7 (Лісп)
;; Двійкове дерево пошуку
;; -------------------------------

;; Структура вузла дерева
(defstruct bst-node
  value
  count
  left
  right)

;; -------------------------------
;; Рекурсивна вставка
(defun bst-insert-rec (node x)
  (cond
    ((null node) (make-bst-node :value x :count 1))
    ((= x (bst-node-value node))
     (incf (bst-node-count node)) node)
    ((< x (bst-node-value node))
     (setf (bst-node-left node)
           (bst-insert-rec (bst-node-left node) x)) node)
    (t
     (setf (bst-node-right node)
           (bst-insert-rec (bst-node-right node) x)) node)))

;; -------------------------------
;; Ітеративна вставка
(defun bst-insert-iter (root x)
  (if (null root)
      (make-bst-node :value x :count 1)
      (let ((current root))
        (loop
          (cond
            ((= x (bst-node-value current))
             (incf (bst-node-count current)) (return root))
            ((< x (bst-node-value current))
             (if (null (bst-node-left current))
                 (setf (bst-node-left current)
                       (make-bst-node :value x :count 1))
                 (setf current (bst-node-left current))))
            (t
             (if (null (bst-node-right current))
                 (setf (bst-node-right current)
                       (make-bst-node :value x :count 1))
                 (setf current (bst-node-right current)))))) root)))

;; -------------------------------
;; Inorder-обхід (ліворуч → корінь → праворуч)
(defun bst-inorder (node)
  (when node
    (bst-inorder (bst-node-left node))
    (format t "~A(~A) " (bst-node-value node) (bst-node-count node))
    (bst-inorder (bst-node-right node))))


;; -------------------------------
;; Приклад використання
(defun demo ()
  (let* ((numbers '(7 3 9 3 11 7 2 5))
         (tree (reduce #'bst-insert-rec numbers :initial-value nil)))
    (format t "Inorder traversal: ")
    (bst-inorder tree)
    (format t "~%")))

;; Виклик прикладу після визначень
(demo)





;; -------------------------------
;; Завантаження чисел з файлу
; (defun load-numbers-from-file (filename)
;   (with-open-file (stream filename)
;     (loop for num = (read stream nil nil)
;           while num
;           collect num)))
; (let* ((numbers '(7 3 9 3 11 7 2 5)) ;; можна замінити на (load-numbers-from-file "input.txt")
