---
layout: post
title: Parallelizing the parsing
---
When processing large log files, I faced the problem of the insufficient speed of my method. There are many places to be improved, but I decided to start with the parallelizing it and then analyze the algorithm in detail.

As the parser reads log file line-by-line, the first idea was to parallelize it by lines. However, as I have already described in the previous post, there are multi-line-lines. If we split the file in groups of lines, we may divide such lines and they won't be processed correctly. So, for start I decided to parallelize the parsing by the files.

## Multiprocessing tool
```python
from multiprocessing import Manager, Pool
```
The multiprocessing module allows to spawn processes in the same manner than you can spawn threads with the threading module. The multiprocessing package includes API, and there is a Pool class that can be used to parallelize executing a function across multiple inputs. I'd like to show how simple is to do this.


#### Pool
```python
with Pool(processes=5) as pool:
    worker = pool.imap(func, run_args)
    for res in worker:
    	print(res)
```
Here I decided to parallelize the executing in 5 threads, and the result in returning to the variable `worker`. The returned values are sorted in their original order. I could stop on this stage, but there was a problem. I used a file descriptor for saving the parser's messages, it could be `stdout` or `stderr` streams, or any text file. The descriptor can't be shared between the processes, and I've found the solution.


#### Queue
There are many ways to organize communication between processes, and I choose the existing in the `multiprocessing` library class `Manager`. It controls a server process which holds Python objects and allows other processes to manipulate them using proxies. A manager returned by `Manager()` supports many types, and one of them  is `Queue`. Processes write to the queue and then I get all the written messages and can put them to the needed file.

```python
m = Manager()
q = m.Queue()
run_args = [[q, i, filenames, path] for i in idxs]
#...
while not q.empty():
    warn = q.get()
    print(warn)
```

## Progressbars
I decided to add a progress bar for the parsing process. I used a [Progressbar](https://pypi.python.org/pypi/progressbar2) library, which can be installed via `pip install progressbar2`. 

```python
import progressbar
```
This library is also easy in use, and I'd like to show the example of creating the progress bar in my task.

#### Progress bar for parsing

```python
widget_style = ['All: ', progressbar.Percentage(), ' (',
                         progressbar.SimpleProgress(), ')', ' ',
                         progressbar.Bar(), ' ', progressbar.Timer(), ' ',
                         progressbar.AdaptiveETA()]
bar = ProgressBar(widgets=widget_style)
with Pool(processes=5) as pool:
    worker = pool.imap(star, run_args)
    for _ in bar(run_args):
        result += [worker.next()]
```

#### Progress bar for sub-processes
There can be situations when one of the log files is bigger then the others, and it is useful to know how many lines are already parsed in each file. The idea was to add a progressbar to each process, and also keep a main progress bar. Since one log message is not always located in the one line, I decided to measure the progress in symbols, counting them with `file.seek(0, os.SEEK_END)`. The part of the solution is presented below, and I used a curses interface to display the progress bars in console.

```python
# creating progressbars for subprocesses
def runner_parallel(inp):
    function, args, name, queue, order_idx = inp
    idx = int(multiprocessing.current_process().name.split("-")[1])
    custom_text = progressbar.FormatCustomText(
                            '{} - %(type_op)s: '.format(name),
                            dict(type_op="Start"))
    widget_style = [custom_text, progressbar.Percentage(), ' (',
                    progressbar.SimpleProgress(), ')', ' ',
                    progressbar.Bar(), ' ', progressbar.Timer(), ' ',
                    progressbar.AdaptiveETA()]
    args += [ProgressBar(widgets=widget_style, fd=Writer((0, idx - 1),
                         queue)), custom_text]
    return (function(*args), order_idx)

# ...in the main
manager = multiprocessing.Manager()
the_queue = manager.Queue()
result = []
widget_style = ['All: ', progressbar.Percentage(), ' (',
                progressbar.SimpleProgress(), ')', ' ',
                progressbar.Bar(), ' ', progressbar.Timer(), ' ',
                progressbar.AdaptiveETA()]
run_args = [(func, args, name, the_queue, order_idx)
            for order_idx, (func, name, args) in enumerate(run_args)]
main_pb = ProgressBar(widgets=widget_style, fd=Writer((0, 0)),
					  max_value=len(run_args))
with Pool(processes=5) as pool:
    workers = pool.imap_unordered(runner_parallel, run_args)
    idx = 0
    main_pb.start()
    while True:
        try:
            try:
                while True:
                    result.append(workers.next(0))
                    idx += 1
                    main_pb.update(idx)
            except multiprocessing.TimeoutError:
                pass
            while not the_queue.empty():
                pos, text = the_queue.get()
   				# print the progress
            time.sleep(1)
        except StopIteration:
            break
result = sorted(result, key=lambda x: x[1])
return [r[0] for r in result]
```
And here is how it looks:
![ProgressPool]({{ site.url }}/assets/progress_pool.png){:style="margin-bottom: 15px;"}

## Conclusion
The use of multiprocessing helps me to decrease the time of parsing log files, even with parallelizing by files. I previously implemented parallelization only in the course "Operating systems". The task was to write Unix shell using C language. Some commands, for example `dir`, `tale` we had to write ourselves, others were calling from the our shell. The most difficult part was the creation of a conveyor (`|` symbol), then the processes were created and executed without waiting for their completion. I will never forget the `WNOHANG` flag in the `waitpid` command, and how our teacher was asking us about the details and definition of this flag for tracking zombie processes. It was interesting and useful to learn the principle of parallel processes and communication between them, as well as signal redefinition and the use of semaphores, messages and shared memory. But now how nice is to use a `Pool` and do all this complex actions in one line! :)