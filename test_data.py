import json


from data import DataModifier

todo_path = r'CSV\todo_test.csv'
done_path = r'CSV\done_test.csv'
conjunctions_path = r'CSV\conj_test.csv'


modifier = DataModifier(todo_path=todo_path,
                        done_path=done_path,
                        conjunctions_path=conjunctions_path
                        )


def test_init():
    assert modifier.todo_path == todo_path
    assert modifier.done_path == done_path
    assert modifier.conjunctions_path == conjunctions_path
    todos = open(todo_path, 'r').read().split('\n')
    done = open(done_path, 'r').read().split('\n')
    if modifier._check_file_empty(todo_path):
        assert modifier.todos == []
    else:
        assert modifier.todos == [json.loads(todo) for todo in todos]

    if modifier._check_file_empty(done_path):
        assert modifier.done == []
    else:
        assert modifier.done == [json.loads(todo) for todo in done]

def test_write_todos():
    year = 2020
    month = 12
    day = 4
    hour = 4
    minute1 = 2
    minute2 = 4
    second = 0
    todo_dict1 = {'year' : year,
                    'month' : month,
                    'day' : day,
                    'hour' : hour,
                    'minute' : minute1,
                    'second' : second}
    todo_dict2 = {'year' : year,
                    'month' : month,
                    'day' : day,
                    'hour' : hour,
                    'minute' : minute2,
                    'second' : second}
    
    modifier.write_todo(**todo_dict1)
    modifier.write_todo(**todo_dict2)
    modifier.is_done()
    assert modifier.todos == []
    done_json_list = open(done_path, 'r').read().split('\n')
    done_dict_list = [json.loads(todo) for todo in done_json_list]
    assert modifier.done == done_dict_list
