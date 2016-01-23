#include <unistd.h>
#include <string.h>

int puts(const char *str) {
  write(1, "I would like to say:\n", 22);
  write(1, str, strlen(str));
  write(1, "\n", 1);
  return 0;
}
