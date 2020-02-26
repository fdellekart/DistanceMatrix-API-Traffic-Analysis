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