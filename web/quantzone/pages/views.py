from django.shortcuts import render

from nodes.models import Subject, Node, NodeRelation, SubjectTag
import json
import networkx as nx
from networkx.readwrite import json_graph


# Create your views here.
def index_view(request):
    subjects = Subject.objects.all().order_by('pk')
    return render(request, 'index.html', {'subjects': subjects})


# Create your views here.
def landing_view(request, landing_id):
    subjects = Subject.objects.all().order_by('pk')
    tpl_str = u'landings/lp_{}.html'.format(landing_id)
    return render(request, tpl_str, {'subjects': subjects})


def graph_view(request):
    all_node_relations = NodeRelation.objects.all()

    dg = nx.DiGraph()

    for relation in all_node_relations:
        dg.add_edge(str(relation.parent), str(relation.child))

    data = json_graph.node_link_data(dg)
    s = json.dumps(data)

    # f = open("fixtures/feb17/me.txt", 'r')
    # print(f)
    # text = f.read()
    # arr = text.split('\n')
    # tag = SubjectTag.objects.get(pk=2)
    # for unit in arr:
    #     Node.objects.create(title=unit, subject_tag=tag)




    return render(request, 'graph.html', {'s': s})
