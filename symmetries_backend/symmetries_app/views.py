import json
from ast import literal_eval

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .symmetries_code import test
from .symmetries_code import gap
from django.http import StreamingHttpResponse

from .symmetries_code.cycle_notation import CycleNotation
from .symmetries_code.graph import Graph
from .symmetries_code.vis import create_graph_pyvis


@api_view(['GET'])
def get_asym_data(request, _id):
    response = StreamingHttpResponse(test.run(_id))
    response.streaming = True
    return response


@api_view(['GET'])
def get_group_info(request):
    data = json.loads(request.query_params.get('data'))
    cycles = set()
    identity = None
    for cycle in data:
        tuples = [tuple(map(int, list(str(literal_eval(c))))) for c in cycle.split('v')]
        cycle_rep = CycleNotation(cycle=tuples)
        gap_repr = cycle_rep.gap_repr()
        if len(gap_repr):
            cycles.add(gap_repr)
        else:
            identity = cycle
    gap_input = 'PrintTo("output_test.txt", "");' \
                'g := Group(' + ','.join(cycles) + '); desc:=StructureDescription(g); AppendTo("output_test.txt", desc);'
    gap.get_group_info(gap_input)
    with open('output_test.txt', 'r') as file:
        group_type = file.read()
        g = Graph(aut_group=cycles, group_type=group_type)
        return Response({'groupType': group_type, 'identity': identity, 'groupDesc': g.group_desc()})


@api_view(['GET'])
def get_custom_graphvis(request):
    vis = create_graph_pyvis(Graph(get_graph_values(request.query_params.get('data'))), True)
    return Response({'vis': vis})


@api_view(['GET'])
def get_custom_graph_symmetries(request):
    graph = Graph(get_graph_values(request.query_params.get('data')))
    # graph = Graph({1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6}, 6: {5, 7}, 7: {6}})
    response = StreamingHttpResponse(test.run(graph=graph))
    response.streaming = True
    return response


def get_graph_values(data):
    data = json.loads(data)
    new_data = dict()
    for i in range(len(data)):
        new_data[i + 1] = set(data[i])
    return new_data
