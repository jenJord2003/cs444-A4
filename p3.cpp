#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
#include "p3.h"
//g++ main.cpp p3.cpp -Wall -Wuninitialized -o a.out
//fails when copy or destruct is called
using namespace std;

Person::Person() {
    first = "";
    last = "";
    height = 0;
    weight = 0;
    prevHeight = nullptr;
    nextHeight = nullptr;
    nextWeight = nullptr;
}
Person::Person(std::string first, std::string last, int height, int weight) {
    this->first = first;
    this->last = last;
    this->height = height;
    this->weight = weight;
    score = 0;
    weightScore = 0;
    prevWeight = nullptr;
    prevHeight = nullptr;
    nextHeight = nullptr;
    nextWeight = nullptr;
}


// PersonList Class Definitions
PersonList::PersonList() {
    headHeightList = nullptr;
    headWeightList = nullptr;
    curr = nullptr;
    tailHeightList = nullptr;
    tailWeightList = nullptr;
    size = 0;
}

int PersonList::getSize()
{
    return this->size;
}

void PersonList::printByHeight(std::ostream& os) {
    //os << "Printing list by height:" << std::endl;
    
    // sort the list in descending order of height using insertion sort
    Person *sorted = nullptr;
    Person *curr = headHeightList;
    while (curr != nullptr) {
        Person *next = curr->nextHeight;
        if (sorted == nullptr || curr->height > sorted->height) {
            curr->nextHeight = sorted;
            sorted = curr;
        } else {
            Person *temp = sorted;
            while (temp->nextHeight != nullptr && curr->height < temp->nextHeight->height) {
                temp = temp->nextHeight;
            }
            curr->nextHeight = temp->nextHeight;
            temp->nextHeight = curr;
        }
        curr = next;
    }

    // print the sorted list
    curr = sorted;
    while (curr != nullptr) {
        os << curr->first << " " << curr->last << ": height=" << curr->height << ", weight=" << curr->weight << std::endl;
        curr = curr->nextHeight;
    }
}

void PersonList::printByWeight(ostream &os) {
    //os << "List ordered by weight:" << endl;
    Person* curr = this->tailWeightList;
    while (curr != nullptr) {
        os << curr->first << " " << curr->last << ": height=" << curr->height << ", weight=" << curr->weight << endl;
        curr = curr->prevWeight;
    }
}

//   DEFAULT
bool PersonList::add(std::string first, std::string last, int height, int weight) {
    // check if the person already exists in the list
    if (exists(first, last)) {
        return false;
    }

    // create a new person with the given information
    Person* newPerson = new Person(first, last, height, weight);

    // calculate the score for the new person based on their height and weight
    double score = height - sqrt(weight) / 10.0;

    // case 1: the list is empty
    if (headHeightList == nullptr) {
        headHeightList = newPerson;
        tailHeightList = newPerson;
        headWeightList = newPerson;
        tailWeightList = newPerson;
        size++;
        return true;
    }

    // find the position to insert the new person based on their score
    Person* curr = headHeightList;
    while (curr != nullptr) {
        double currScore = curr->height - sqrt(curr->weight) / 10.0;
        if (score > currScore) {
            // insert new person before the current person in the height list
            newPerson->nextHeight = curr;
            newPerson->prevHeight = curr->prevHeight;
            if (curr->prevHeight != nullptr) {
                curr->prevHeight->nextHeight = newPerson;
            } else {
                headHeightList = newPerson;
            }
            curr->prevHeight = newPerson;

            // insert new person before the current person in the weight list
            newPerson->nextWeight = curr;
            newPerson->prevWeight = curr->prevWeight;
            if (curr->prevWeight != nullptr) {
                curr->prevWeight->nextWeight = newPerson;
            } else {
                headWeightList = newPerson;
            }
            curr->prevWeight = newPerson;
            size++;
            return true;
        }
        curr = curr->nextHeight;
    }

    // add the new person to the end of the height list if their score is lower than all existing persons
    newPerson->prevHeight = tailHeightList;
    tailHeightList->nextHeight = newPerson;
    tailHeightList = newPerson;

    // add the new person to the end of the weight list if their score is higher than all existing persons
    newPerson->prevWeight = tailWeightList;
    tailWeightList->nextWeight = newPerson;
    tailWeightList = newPerson;

    size++;
    return true;
}


bool PersonList::exists(std::string first, std::string last) {
    Person* curr = headHeightList;
    while (curr != nullptr) {
        if (curr->first == first && curr->last == last) {
            return true;
        }
        curr = curr->nextHeight;
    }
    return false;
}


int PersonList::getHeight(string first, string last) 
{
    Person *curr = this->headHeightList;
    while (curr != nullptr) 
    {
        if (curr->first == first && curr->last == last) 
        {
            return curr->height;
        }
        curr = curr->nextHeight;
    }
    // if person not found
    return -1;
}


int PersonList::getWeight(string first, string last) 
{
    Person* curr = this->headWeightList;
    while (curr != nullptr) 
    {
        if (curr->first == first && curr->last == last) 
        {
            return curr->weight;
        }
        curr = curr->nextHeight;
    }
    return -1;
}



bool PersonList::remove(string first, string last) {
    Person *curr = this->headHeightList;
    Person *prev = nullptr;
    bool found = false;
    
    // Search for the node to remove in the height list
    while (curr != nullptr && !found) {
        if (curr->first == first && curr->last == last) {
            found = true;
            if (prev == nullptr) {
                // Removing the head node
                this->headHeightList = curr->nextHeight;
            } else {
                prev->nextHeight = curr->nextHeight;
            }
            if (curr->nextHeight != nullptr) {
                curr->nextHeight->prevHeight = prev;
            }
            if (tailHeightList == curr) {
                tailHeightList = prev;
            }
            curr->prevHeight = nullptr;
            curr->nextHeight = nullptr;
        } else {
            prev = curr;
        }
        curr = curr->nextHeight;
    }
    
    if (!found) {
        // Node not found in list
        return false;
    }
    
    // Search for the node to remove in the weight list
    curr = this->headWeightList;
    prev = nullptr;
    while (curr != nullptr) {
        if (curr->first == first && curr->last == last) {
            if (prev == nullptr) {
                // Removing the head node
                this->headWeightList = curr->nextWeight;
            } else {
                prev->nextWeight = curr->nextWeight;
            }
            if (curr->nextWeight != nullptr) {
                curr->nextWeight->prevWeight = prev;
            }
            if (tailWeightList == curr) {
                tailWeightList = prev;
            }
            delete curr;
            this->size--;
            return true;
        } else {
            prev = curr;
        }
        curr = curr->nextWeight;
    }
    
    // Node not found in weight list (should never happen)
    return false;
}


bool PersonList::updateName(std::string oldFirst, std::string oldLast, std::string newFirst, std::string newLast) {
    if (!exists(oldFirst, oldLast)) {
        return false;
    }
    Person* curr = headHeightList;
    while (curr != nullptr) {
        if (curr->first == oldFirst && curr->last == oldLast) {
            curr->first = newFirst;
            curr->last = newLast;
            return true;
        }
        curr = curr->nextHeight;
    }
    return false;
}

// DEFAULT for height
bool PersonList::updateHeight(std::string first, std::string last, int newHeight) {
    if (!exists(first, last)) {
        return false;
    }
    Person* curr = headHeightList;
    while (curr != nullptr) {
        if (curr->first == first && curr->last == last) {
            // remove the person from the list
            if (curr->prevHeight == nullptr) {
                headHeightList = curr->nextHeight;
            } else {
                curr->prevHeight->nextHeight = curr->nextHeight;
            }
            if (curr->nextHeight == nullptr) {
                tailHeightList = curr->prevHeight;
            } else {
                curr->nextHeight->prevHeight = curr->prevHeight;
            }
            // update the height and re-insert the person into the list
            curr->height = newHeight;
            double score = curr->height - sqrt(curr->weight) / 10.0;
            if (headHeightList == nullptr || score > headHeightList->height - sqrt(headHeightList->weight) / 10.0) {
                curr->prevHeight = nullptr;
                curr->nextHeight = headHeightList;
                if (headHeightList != nullptr) {
                    headHeightList->prevHeight = curr;
                } else {
                    tailHeightList = curr;
                }
                headHeightList = curr;
            } else {
                Person* temp = headHeightList;
                while (temp->nextHeight != nullptr && score <= temp->nextHeight->height - sqrt(temp->nextHeight->weight) / 10.0) {
                    temp = temp->nextHeight;
                }
                curr->prevHeight = temp;
                curr->nextHeight = temp->nextHeight;
                if (temp->nextHeight != nullptr) {
                    temp->nextHeight->prevHeight = curr;
                } else {
                    tailHeightList = curr;
                }
                temp->nextHeight = curr;
            }
            return true;
        }
        curr = curr->nextHeight;
    }
    return false;
}


bool PersonList::updateWeight(std::string first, std::string last, int newWeight) {
    Person *curr = headWeightList;
    while (curr != nullptr) {
        if (curr->first == first && curr->last == last) {
            // remove the person from the weight list
            if (curr->prevWeight == nullptr) {
                headWeightList = curr->nextWeight;
            } else {
                curr->prevWeight->nextWeight = curr->nextWeight;
            }
            if (curr->nextWeight == nullptr) {
                tailWeightList = curr->prevWeight;
            } else {
                curr->nextWeight->prevWeight = curr->prevWeight;
            }

            // update the weight and re-insert the person into the weight list
            curr->weight = newWeight;
            Person* temp = headWeightList;
            while (temp != nullptr && newWeight <= temp->weight) {
                temp = temp->nextWeight;
            }

            if (temp == headWeightList) {
                curr->prevWeight = nullptr;
                curr->nextWeight = headWeightList;
                headWeightList->prevWeight = curr;
                headWeightList = curr;
            } else if (temp == nullptr) {
                curr->prevWeight = tailWeightList;
                curr->nextWeight = nullptr;
                tailWeightList->nextWeight = curr;
                tailWeightList = curr;
            } else {
                curr->prevWeight = temp->prevWeight;
                curr->nextWeight = temp;
                temp->prevWeight->nextWeight = curr;
                temp->prevWeight = curr;
            }

            return true;
        }
        curr = curr->nextWeight;
    }
    return false;
}


//destruct
PersonList::~PersonList() {
    // Delete all nodes in headHeightList
    while (headHeightList != nullptr) {
        //cout << "Debug 1" << endl;
        Person* temp = headHeightList;
        //cout << "Debug 2" << endl;
        headHeightList = headHeightList->nextHeight;
        //cout << "Debug 3" << endl;
        delete temp;
        //cout << "Debug 4" << endl;
    }
   // Reset head and tail pointers to null
    //cout << "Debug 8" << endl;
    headHeightList = nullptr;
    headWeightList = nullptr;
    tailHeightList = nullptr;
    tailWeightList = nullptr;
}


const PersonList& PersonList::operator=(const PersonList& src) {
    // Check for self-assignment
    if (this == &src) {
        return *this;
    }

    // Call deepCopy to clear the current list and copy the contents of the source list
    deepCopy(src);

    return *this;
}


//copycon
PersonList::PersonList(const PersonList& src) {
    // Initialize variables
    headHeightList = nullptr;
    headWeightList = nullptr;
    tailHeightList = nullptr;
    tailWeightList = nullptr;
    size = 0;

    // Call deepCopy to get a deepcopy of the source list
    deepCopy(src);
}


PersonList& PersonList::deepCopy(const PersonList& src) {
    // Clear the current list
    Person* curr = headHeightList;
    while (curr != nullptr) {
        Person* temp = curr;
        curr = curr->nextHeight;
        delete temp;
    }
    headHeightList = nullptr;
    headWeightList = nullptr;
    tailHeightList = nullptr;
    tailWeightList = nullptr;
    size = 0;

    // Copy contents of the source list to the current list
    for (Person* curr = src.headHeightList; curr != nullptr; curr = curr->nextHeight) {
        // Use the add function to add the person, maintaining the correct order
        add(curr->first, curr->last, curr->height, curr->weight);
    }

    return *this;
}
