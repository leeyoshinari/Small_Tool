# timeoutLimit
It's used to avoid function run stuck.

When a function runs for a long time, or running is stuck but no error, you need to determine whether the function runs timeout. If timeout, jumping out of the function and some messages should be returned.

With the Python decorator, it's possible to use a timing function without affecting the original function.

## Usage
1. clone timeoutLimit repository
   ```shell
   git clone https://github.com/leeyoshinari/Small_Tool.git
   
   cd Small_Tool/timeoutLimit
   ```

2. Example
   ```shell
   import time
   from xxx/timeout import timeoutlimit
   
   @timeoutlimit(3)
   def sleep():
       time.sleep(5)
       return True
	
   print(sleep())
   ```

## Others
   If a function runs timeout, it raises `Exception`, else, it returns the result of the function.
