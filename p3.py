# p3.py
# Python translation of the C++ Person / PersonList project.
# Maintains two doubly linked lists: one sorted by height (desc), one by weight (desc).

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Iterable, Tuple, List, Any


@dataclass
class Person:
    first: str
    last: str
    height: int
    weight: int
    score: float = 0.0
    weightScore: float = 0.0

    # Pointers for height-sorted list
    prevHeight: Optional['Person'] = field(default=None, repr=False)
    nextHeight: Optional['Person'] = field(default=None, repr=False)

    # Pointers for weight-sorted list
    prevWeight: Optional['Person'] = field(default=None, repr=False)
    nextWeight: Optional['Person'] = field(default=None, repr=False)

    def key_height(self) -> Tuple[int, str, str]:
        # Sort primarily by height (desc), then by last/first for stability
        return (-self.height, self.last, self.first)

    def key_weight(self) -> Tuple[int, str, str]:
        # Sort primarily by weight (desc)
        return (-self.weight, self.last, self.first)

    def name_tuple(self) -> Tuple[str, str]:
        return (self.first, self.last)


class PersonList:
    def __init__(self) -> None:
        self.headHeightList: Optional[Person] = None
        self.tailHeightList: Optional[Person] = None
        self.headWeightList: Optional[Person] = None
        self.tailWeightList: Optional[Person] = None
        self.size: int = 0

    # ---- utilities -------------------------------------------------------
    def _find_by_name(self, first: str, last: str) -> Optional[Person]:
        cur = self.headHeightList
        while cur:
            if cur.first == first and cur.last == last:
                return cur
            cur = cur.nextHeight
        return None

    def exists(self, first: str, last: str) -> bool:
        return self._find_by_name(first, last) is not None

    def getSize(self) -> int:
        return self.size

    # ---- insert helpers (height / weight) --------------------------------
    def _insert_height(self, p: Person) -> None:
        if not self.headHeightList:
            self.headHeightList = self.tailHeightList = p
            p.prevHeight = p.nextHeight = None
            return
        cur = self.headHeightList
        while cur and p.key_height() > cur.key_height():
            cur = cur.nextHeight
        if cur is self.headHeightList:
            # insert at head
            p.prevHeight = None
            p.nextHeight = self.headHeightList
            self.headHeightList.prevHeight = p
            self.headHeightList = p
        elif cur is None:
            # insert at tail
            p.prevHeight = self.tailHeightList
            p.nextHeight = None
            self.tailHeightList.nextHeight = p
            self.tailHeightList = p
        else:
            # insert before cur (middle)
            p.prevHeight = cur.prevHeight
            p.nextHeight = cur
            assert cur.prevHeight is not None
            cur.prevHeight.nextHeight = p
            cur.prevHeight = p

    def _insert_weight(self, p: Person) -> None:
        if not self.headWeightList:
            self.headWeightList = self.tailWeightList = p
            p.prevWeight = p.nextWeight = None
            return
        cur = self.headWeightList
        while cur and p.key_weight() > cur.key_weight():
            cur = cur.nextWeight
        if cur is self.headWeightList:
            # insert at head
            p.prevWeight = None
            p.nextWeight = self.headWeightList
            self.headWeightList.prevWeight = p
            self.headWeightList = p
        elif cur is None:
            # insert at tail
            p.prevWeight = self.tailWeightList
            p.nextWeight = None
            self.tailWeightList.nextWeight = p
            self.tailWeightList = p
        else:
            # insert before cur (middle)
            p.prevWeight = cur.prevWeight
            p.nextWeight = cur
            assert cur.prevWeight is not None
            cur.prevWeight.nextWeight = p
            cur.prevWeight = p

    # ---- remove helpers (height / weight) --------------------------------
    def _unlink_height(self, p: Person) -> None:
        if p.prevHeight:
            p.prevHeight.nextHeight = p.nextHeight
        else:
            self.headHeightList = p.nextHeight
        if p.nextHeight:
            p.nextHeight.prevHeight = p.prevHeight
        else:
            self.tailHeightList = p.prevHeight
        p.prevHeight = p.nextHeight = None

    def _unlink_weight(self, p: Person) -> None:
        if p.prevWeight:
            p.prevWeight.nextWeight = p.nextWeight
        else:
            self.headWeightList = p.nextWeight
        if p.nextWeight:
            p.nextWeight.prevWeight = p.prevWeight
        else:
            self.tailWeightList = p.prevWeight
        p.prevWeight = p.nextWeight = None

    # ---- public API ------------------------------------------------------
    def add(self, first: str, last: str, height: int, weight: int) -> bool:
        if self.exists(first, last):
            return False
        p = Person(first, last, int(height), int(weight))
        self._insert_height(p)
        self._insert_weight(p)
        self.size += 1
        return True

    def remove(self, first: str, last: str) -> bool:
        p = self._find_by_name(first, last)
        if not p:
            return False
        self._unlink_height(p)
        self._unlink_weight(p)
        self.size -= 1
        return True

    def getHeight(self, first: str, last: str) -> int:
        p = self._find_by_name(first, last)
        return p.height if p else -1

    def getWeight(self, first: str, last: str) -> int:
        # search weight list (fast if many with same height)
        cur = self.headWeightList
        while cur:
            if cur.first == first and cur.last == last:
                return cur.weight
            cur = cur.nextWeight
        return -1

    def updateName(self, oldFirst: str, oldLast: str, newFirst: str, newLast: str) -> bool:
        p = self._find_by_name(oldFirst, oldLast)
        if not p:
            return False
        if (oldFirst, oldLast) != (newFirst, newLast) and self.exists(newFirst, newLast):
            # avoid duplicates
            return False
        p.first, p.last = newFirst, newLast
        return True

    def _reposition_after_height_change(self, p: Person) -> None:
        # unlink then reinsert in height list
        self._unlink_height(p)
        self._insert_height(p)

    def _reposition_after_weight_change(self, p: Person) -> None:
        self._unlink_weight(p)
        self._insert_weight(p)

    def updateHeight(self, first: str, last: str, newHeight: int) -> bool:
        p = self._find_by_name(first, last)
        if not p:
            return False
        p.height = int(newHeight)
        self._reposition_after_height_change(p)
        return True

    def updateWeight(self, first: str, last: str, newWeight: int) -> bool:
        p = self._find_by_name(first, last)
        if not p:
            return False
        p.weight = int(newWeight)
        self._reposition_after_weight_change(p)
        return True

    # ---- printing (does not mutate structure) ----------------------------
    def iter_by_height(self) -> Iterable[Person]:
        cur = self.headHeightList
        while cur:
            yield cur
            cur = cur.nextHeight

    def iter_by_weight(self) -> Iterable[Person]:
        cur = self.headWeightList
        while cur:
            yield cur
            cur = cur.nextWeight

    def printByHeight(self) -> str:
        lines = []
        for p in self.iter_by_height():
            lines.append(f"{p.first} {p.last}: height={p.height}, weight={p.weight}")
        return "\n".join(lines)

    def printByWeight(self) -> str:
        lines = []
        for p in self.iter_by_weight():
            lines.append(f"{p.first} {p.last}: height={p.height}, weight={p.weight}")
        return "\n".join(lines)

    # ---- copying ---------------------------------------------------------
    def deepCopy(self, src: 'PersonList') -> 'PersonList':
        # Clear current
        self.__init__()
        # Copy each person in height order to preserve both orders via add()
        for p in src.iter_by_height():
            self.add(p.first, p.last, p.height, p.weight)
        return self

    def copy(self) -> 'PersonList':
        new = PersonList()
        new.deepCopy(self)
        return new

    # Python dunder helpers
    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterable[Person]:
        return self.iter_by_height()

    def __repr__(self) -> str:
        return f"PersonList(size={self.size})"


if __name__ == "__main__":
    # Simple manual test / demo
    pl = PersonList()
    pl.add("Alice", "Zephyr", 65, 140)
    pl.add("Bob", "Yellow", 70, 180)
    pl.add("Carol", "Xavier", 62, 150)
    pl.add("Dave", "Williams", 70, 175)

    print("By height (desc):")
    print(pl.printByHeight(), "\n")

    print("By weight (desc):")
    print(pl.printByWeight(), "\n")

    print("Update Dave weight to 200...")
    pl.updateWeight("Dave", "Williams", 200)
    print(pl.printByWeight(), "\n")

    print("Remove Alice Zephyr...")
    pl.remove("Alice", "Zephyr")
    print(pl.printByHeight())
