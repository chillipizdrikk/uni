#pragma once

namespace algo
{
	template<typename T>
	class List
	{
	private:
		struct Element
		{
			T value;
			Element* next;

			Element(const T& v)
			:value(v), next(nullptr) {}
		};
		static const size_t DEFAULT_SIZE = 10;
		Element* begin;
		Element* end;
		size_t size;

	public:
		List()
			:begin(nullptr), end(nullptr), size(0) {}
		~List()
		{
			while (begin)
			{
				Element* arr = begin;
				begin = begin->next;
				delete arr;
			}
		}
		void AddFront(const T& val);
		void AddBack(const T& val);

		class Iterator {
		private:
			Element* iter;
		public:
			Iterator(Element* iter = nullptr) 
				: iter(iter) {}

			T& operator*() const { return iter->value; }
			Iterator& operator++() { iter = iter->next; return *this; }

			bool operator==(const Iterator& it)const { return iter == it.iter; }
			bool operator!=(const Iterator& it) const { return iter != it.iter; }
		};

		Iterator Begin() const { return Iterator(begin); }
		Iterator End() const { return Iterator(nullptr); }

	};
	
	template <typename T>
	void List<T>::AddFront(const T& val)
	{
		Element* elem = new Element(val);
		if (begin == nullptr)
		{
			begin = elem;
			end = elem;
		}
		else
		{
			elem->next = begin;
			begin = elem;
		}
		++size;
	}

	template <typename T>
	void List<T>::AddBack(const T& val)
	{
		Element* elem = new Element(val);
		if (begin == nullptr) {
			begin = elem;
			end = elem;
		}
		else {
			end->next = elem;
			end = elem;
		}
		++size;
	}
}