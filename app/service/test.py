from tool import Tool
from construction import Construction
from worker import Worker
from my_exception import checking_incoming_objects, checking_class, MethodError
from managers import ToolManager, WorkerManager, ConstructionManager

t1 = Tool("t1")
t2 = Tool("t2")
t3 = Tool("t3")

c1 = Construction(name="constr1", project="project1")
c2 = Construction(name="constr2", project="project2")
c3 = Construction(name="constr3", project="project3")

w1 = Worker(name="name1", surname="surname1")
w2 = Worker(name="name2", surname="surname2")
w3 = Worker(name="name3", surname="surname3")

m_t1 = ToolManager(t1)
m_t1.filling_fields(construction=c1)
m_t2 = ToolManager(t2)
m_t2.filling_fields(construction=c2)

m_w1 = WorkerManager(w1)
m_w1.set_construction(construction=c1)

m_w2 = WorkerManager(w2)
m_w2.set_construction(construction=c2)

m_c1 = ConstructionManager(construction=c1)
m_c2 = ConstructionManager(construction=c2)

m_c1.replace_person_responsible(new_responsible=w3)
m_c1.close_object(c2)