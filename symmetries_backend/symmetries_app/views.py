import json
import os
import time
from ast import literal_eval

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .symmetries_code import main
from .symmetries_code import gap
from django.http import StreamingHttpResponse

from .symmetries_code.cycle_notation import Cycle
from .symmetries_code.graph import Graph
from .symmetries_code.graphviz import create_graph_pyvis


@api_view(['GET'])
def get_asym_data(request, _id):
    g = main.asymmetric_graphs[_id]
    response = StreamingHttpResponse(main.run(g))
    response.streaming = True
    return response


@api_view(['GET'])
def get_group_info(request):
    data = json.loads(request.query_params.get('data'))
    cycles = set()
    identity = None
    for cycle in data:
        tuples = [tuple(map(int, list(str(literal_eval(c))))) for c in cycle.split('v')]
        cycle_rep = Cycle(cycle=tuples)
        gap_repr = cycle_rep.gap_repr()
        if len(gap_repr):
            cycles.add(gap_repr)
        else:
            identity = cycle
    input_time = str(hash(','.join(cycles))) + str(time.time_ns())
    if input_time[0] == '-':
        input_time = input_time[1:]
    abs_path = os.path.abspath(os.curdir)
    filename_input = abs_path + '/symmetries_app/symmetries_code/gap_files/' + input_time + '.g'
    filename_output = abs_path + '/symmetries_app/symmetries_code/gap_files/output_' + input_time + '.txt'
    gap_input = 'g := Group(' + ','.join(cycles) + '); desc:=StructureDescription(g); ' \
                                                   'path := "' + filename_output + '"; PrintTo(path, desc);'
    gap.get_group_info(gap_input, filename_input)
    with open(filename_output, 'r') as file:
        group_type = file.read()
    g = Graph(aut_group=cycles, group_type=group_type)
    os.remove(filename_input)
    os.remove(filename_output)
    return Response({'groupType': group_type, 'identity': identity, 'groupDesc': g.group_desc()})


@api_view(['GET'])
def get_custom_graphvis(request):
    vis = create_graph_pyvis(get_graph_values(request.query_params.get('data')), True)
    return Response({'vis': vis})


@api_view(['GET'])
def get_graphvis(request):
    data = json.loads(request.query_params.get('data'))
    data = {int(key): value for key, value in data.items()}
    vis = create_graph_pyvis(data)
    return Response({'vis': vis})


@api_view(['GET'])
def get_asym_vis(request):
    vis = create_graph_pyvis(main.asymmetric_graphs[request.query_params.get('data')].data, labels=True)
    return Response({'vis': vis})


@api_view(['GET'])
def get_custom_graph_symmetries(request):
    graph = Graph(get_graph_values(request.query_params.get('data')))
    response = StreamingHttpResponse(main.run(graph=graph))
    response.streaming = True
    return response


def get_graph_values(data):
    data = json.loads(data)
    new_data = dict()
    for i in range(len(data)):
        new_data[i + 1] = set(data[i])
    return new_data


@api_view(['GET'])
def get_petersen_symmetries(request):
    graph = Graph({1: {3, 4, 6}, 2: {4, 5, 7}, 3: {1, 5, 8}, 4: {1, 2, 9}, 5: {2, 3, 10}, 6: {1, 7, 10}, 7: {2, 6, 8}, 8: {3, 7, 9}, 9: {4, 8, 10}, 10: {5, 6, 9}})
    response = StreamingHttpResponse(main.run(graph=graph))
    response.streaming = True
    return response
