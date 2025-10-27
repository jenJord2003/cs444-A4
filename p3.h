#include <string>
struct Person {
  std::string first, last;
  int height, weight;
  double score, weightScore;
  Person *prevHeight, *nextHeight, *prevWeight, *nextWeight;
  Person();
  Person(std::string, std::string, int, int);
};
struct PersonList {
  Person *headHeightList, *headWeightList, *tailHeightList, *tailWeightList, *curr;
  int size;
  PersonList();
  ~PersonList();
  bool add(std::string, std::string, int, int);
  bool remove(std::string, std::string);
  bool exists(std::string, std::string);
  int  getHeight(std::string, std::string);
  int  getWeight(std::string, std::string);
  void printByHeight(std::ostream&);
  void printByWeight(std::ostream&);
  bool updateName(std::string, std::string, std::string, std::string);
  bool updateHeight(std::string, std::string, int);
  bool updateWeight(std::string, std::string, int);
  int  getSize();
  const PersonList& operator=(const PersonList& src);
  PersonList(const PersonList& src);
  PersonList& deepCopy(const PersonList& src);
};
