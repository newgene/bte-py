from .transformer import BaseTransformer


class EBIProteinTransformer(BaseTransformer):
    def wrap(self, res):
        new_comments = []
        if res and 'comments' in res:
            for comment in res['comments']:
                if 'reaction' in comment:
                    comment['reaction']['dbReferences'] = [item for item in comment['reaction']['dbReferences'] if item['type'] == 'Rhea']
                new_comments.append(comment)
        res['comments'] = new_comments
        return res
