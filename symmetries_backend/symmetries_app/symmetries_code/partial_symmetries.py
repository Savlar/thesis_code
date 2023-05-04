import json
import math
import multiprocessing

import time


class PartialSymmetries:

    def __init__(self, g, only_full_symmetries=False, use_timer=True, timeout_after=60):
        self.graph = g
        self.chunk = 0
        self.only_full_symmetries = only_full_symmetries
        self.start_size = 0 if not only_full_symmetries else g.vertex_count()
        self.total_partial_symmetries = 0
        self.total_induced_subgraphs = 0
        self.runtime = 0
        self.start = 0
        self.density = self.graph.density()
        self.use_timer = use_timer
        self.timer_process = multiprocessing.Process(target=timer, args=(timeout_after,))
        if self.use_timer:
            self.timer_process.start()

    def get_partial_symmetries(self):
        self.start = time.time()
        for k in reversed(range(self.start_size, self.graph.vertex_count() + 1)):
            if k == 0:
                yield from self.empty_permutation()
            else:
                yield from self.get_data_for_k_vertex_subgraphs(k)
                if self.timed_out():
                    yield json.dumps({'chunk': self.chunk, 'error': 'timeout'})
                    return
        self.kill_timer()

    def get_data_for_k_vertex_subgraphs(self, k):
        type_id = 1 if (self.graph.vertex_count() < 11 or 0.2 > self.density or 0.8 < self.density) else 2
        # type_id = 2
        for subgraph in self.graph.find_isomorphism_classes(k, type_id):
            subgraph.create_d_class()
            self.total_induced_subgraphs += 1
            size = math.pow(len(subgraph.d_class), 2) * len(subgraph.rep.aut_group)
            self.total_partial_symmetries += size
            yield json.dumps({'chunk': self.chunk, 'result': subgraph.d_class, 'vertices': subgraph.rep.vertex_count(),
                              'edges': subgraph.rep.edge_count(), 'size': size, 'graph': subgraph.rep.data},
                             default=list)
            self.chunk += 1

    def empty_permutation(self):
        self.total_partial_symmetries += 1
        yield json.dumps({'chunk': self.chunk, 'result': [[{'data': ['∅'], 'is_group': False}]],
                          'vertices': 0, 'edges': 0, 'size': 1, 'graph': None})

    def get_number_of_partial_symmetries(self):
        total = 1
        for k in range(1, self.graph.vertex_count() + 1):
            for subgraph in self.graph.find_isomorphism_classes(k):
                self.total_induced_subgraphs += 1
                total += subgraph.size()
        return total

    def timed_out(self):
        if self.use_timer and not self.timer_process.is_alive():
            self.get_runtime()
            return True

    def kill_timer(self):
        self.get_runtime()
        if self.timer_process.is_alive():
            self.timer_process.terminate()

    def get_runtime(self):
        self.runtime = round(time.time() - self.start, 3)

    def clear(self):
        self.__init__(self.graph, self.only_full_symmetries, self.use_timer)

def timer(timeout_after=60):
    time.sleep(timeout_after)
