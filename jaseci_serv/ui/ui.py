"""
Jaseci UI iterface to Jaseci backend
"""
from django.shortcuts import render
from django.http import HttpResponse
from jaseci.graph.node import node
from jaseci.graph.edge import edge
from jaseci.graph.graph import graph
from jaseci.actor.sentinel import sentinel
from django.contrib.auth import get_user_model
from jaseci.utils.utils import logger
import uuid
import json


class ui():
    """Main UI Functionality for Jaseci"""

    def __init__(self):
        self.req = None

    def ctx(self):
        return {
            'graphs': self.master.graph_ids.obj_list(),
        }

    def check_dummy_user(self):
        if(not get_user_model().objects.
           filter(email="mars.ninja@gmail.com").count()):
            get_user_model().objects.create_superuser(
                email='mars.ninja@gmail.com',
                password='planetj1',
                name='some dude',
            )

    def check_op(self):
        """Operation router for frontend calls"""
        if('op' in self.req.GET.keys()):
            return getattr(self, self.req.GET['op'])()
        return False

    def create_graph(self):
        """Create graph operation for Jaseci users"""
        self.master.graph_ids.add_obj(
            graph(h=self.master._h, name="Untitled Graph")
        )
        return render(self.req, 'box-assets.html', self.kubctx())

    def create_sentinel(self):
        """Create Sentinel program for Graph """
        graph = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        graph.sentinel_ids.add_obj(
            sentinel(h=graph._h, name="Untitled Sentinel", code='# Jac Code')
        )
        return render(self.req, 'box-assets.html', self.ctx())

    def delete(self):
        """Specail debug tool"""
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        if(isinstance(item.owner(), graph)):
            item.owner().sentinel_ids.destroy_obj(item)
        elif(isinstance(item, graph)):
            item.owner().graph_ids.destroy_obj(item)
        return render(self.req, 'box-assets.html', self.ctx())

    def get_sentinel_code(self):
        """Get the Jac program for a sentinel"""
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        return HttpResponse(item.code)

    def code_update(self):
        """Update code in sentinel based on editor"""
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        item.code = self.req.GET['text']
        item.save()

    def register_code(self):
        """Update code in sentinel based on editor"""
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        item.register_code()
        item.save()
        return render(self.req, 'box-assets.html', self.ctx())

    def render_vis_graph(self):
        target = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        target = target.get_network()
        raw_data = {'nodes': [], 'edges': []}
        for i in target:
            if (isinstance(i, node)):
                if(i.name != 'basic'):
                    raw_data['nodes'].append([i.id.urn, f'{i.kind}:{i.name}'])
                else:
                    raw_data['nodes'].append([i.id.urn, f'{i.kind}'])
            if(isinstance(i, edge)):
                raw_data['edges'].append([i.from_node().id.urn,
                                          i.to_node().id.urn])
        ret = ''
        for i in raw_data['nodes']:
            ret += f"addNode('{i[0]}','{i[1]}');\n"
        for i in raw_data['edges']:
            ret += f"addEdge('{i[0]}','{i[1]}');\n"
        return HttpResponse(ret)

    def prime_walker(self):
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        start_node = self.master._h.get_obj(uuid.UUID(self.req.GET['node']))
        item.prime(start_node)

    def step_walker(self):
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        item.step()
        item.save()
        return HttpResponse(json.dumps(item.report))

    def run_walker(self):
        item = self.master._h.get_obj(uuid.UUID(self.req.GET['id']))
        item.run()
        return HttpResponse(json.dumps(item.report))

    def obj_to_json(self):
        "Present json representation of object as string using Django"
        res = self.master._h.get_obj(
            uuid.UUID(self.req.GET['id'])).json(5)
        # item_id = uuid.UUID(self.req.GET['id'])
        # obj = JaseciObject.objects.get(jid=item_id)
        # res = JaseciObjectSerializer(obj, context={'request': self.req}).data
        # res = JSONRenderer().render(res, renderer_context={'indent': 4})
        return HttpResponse(res)

    def get_console(self):
        return HttpResponse(logger.jaseci_console.getvalue()[-10000:])
