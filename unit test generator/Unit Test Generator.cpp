// Unit Test Generator.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include "NodeUtility.h"
std::ofstream output("auto_generated_unittest.py");
void populate(NodeUtility::Node *cur);
bool verifyuniqueness(NodeUtility::Node *cur, const std::string &name);
int main()
{
    using namespace NodeUtility;
    // prompt the name of the head most ingredient
    std::string head_node_name = "";
    do
    {
        std::cout << "What is the name of the item you want to create?" << std::endl;
        std::getline(std::cin, head_node_name);
        if (head_node_name.empty())
        {
            std::cout << "Please type in something!" << std::endl;
        }
    } while (head_node_name.empty());
    auto head = new Node(head_node_name);
    // prompt subingredients
    populate(head);
    // make ingredient names unique
    /// test this function below the comment
    // prompt desired amount
    std::cout << "How much " << head->ingredient << " do you want to create? " << std::endl;
    int desirednumofhead = integer_input();
    // set assert values - do arithmetic
    NodeUtility::setassertvalues(head, desirednumofhead);
    // create and write into file
    //  create docstring
    write_unittest_module::docstring::module(output);
    output << std::endl;
    // create variable declarations
    write_unittest_module::tree_declaration(output, head);
    output << "reversearithmetic(" << format::formatstring(head->ingredient, format::instance_declaration) << ", " << desirednumofhead << ")" << std::endl;
    output << std::endl
           << std::endl;
    // create test class
    write_unittest_module::createclass(output, head);
    // create test methods
    write_unittest_module::tree_method(output, head);
    // clean up allocated memory from tree
    //create CSV file
    std::string csvfilename = head->ingredient;
    csvfilename = format::formatstring(csvfilename,format::docstring);
    csvfilename.append(".csv");
    //std::ofstream CSVfile(csvfilename);
    std::ofstream CSVfile("test.csv");
    write_CSV_file::writedata(head,CSVfile);
    // terminate process
    massdelete(head);
    output.close();
    return 0;
}
void populate(NodeUtility::Node *cur)
{
    std::cout << "What do you need to create " << cur->ingredient << ":" << std::endl;
    std::string userinput = "";
    std::vector<std::string> userinputs = {};
    auto headnode = cur;
    while (headnode->parent)
    {
        headnode = headnode->parent;
    }
    // prompt inputs
    while (true)
    {
        // check for duplicates
        std::getline(std::cin, userinput);
        bool repeated_local_input = false;                     // input is repeated from the user inputs vector
        bool isunique = verifyuniqueness(headnode, userinput); // input is repeated from the tree and is not unique
        for (const auto &myinput : userinputs)
        {
            repeated_local_input = userinput == myinput;
            if (repeated_local_input)
            {
                break;
            }
        }
        if (userinput.empty())
        {
            break;
        }
        else if (not isunique) // ingredient cannot be typed in already, EACH ingredient input must be unique
        {
            std::cout << "This ingredient name is not unique, please type something on the end of its name to make it unique" << std::endl;
        }
        else if (userinput == cur->ingredient) // ingredient cannot be the same as the augment node
        {
            std::cout << "You cannot type that in!" << std::endl;
        }
        else if (repeated_local_input) // ingredient cannot be repeated
        {
            std::cout << "You already typed that in!" << std::endl;
        }
        else if (userinput == headnode->ingredient and headnode != cur) // ingredient cannot be the same ingredient as the head node
        {
            std::cout << "You cannot type that in, we are trying to make that item!" << std::endl;
        }
        else if (isdigit_check(userinput)) // ingredient cannot be only numbers because it will give variable name errors in the resulted unit test module
        {
            std::cout << "Please type in some letters, an ingredient name with only numbers is not allowed!" << std::endl;
        }
        else // if ingredient is valid use it to create a child node with it
        {
            userinputs.emplace_back(userinput);
        }
    }
    // create child node instances
    bool promptbool = true;
    int amountmadepercraft = 0;
    for (const auto &childname : userinputs)
    {
        if (promptbool)
        {
            auto childinstance = new NodeUtility::Node(childname, cur, 0, 1, 1, promptbool);
            promptbool = false;
            amountmadepercraft = childinstance->amountmadepercraft;
        }
        else
        {
            auto childinstance = new NodeUtility::Node(childname, cur, 0, amountmadepercraft, 1);
        }
    }
    // recursive runtime
    for (auto childnode : cur->children)
    {
        populate(childnode);
    }
}
bool verifyuniqueness(NodeUtility::Node *cur, const std::string &name)
{
    // just traverse the tree and check if the name is the same as any of the ingredient names
    bool isunique = cur->ingredient != name;
    if (isunique)
    {
        for (const auto child : cur->children)
        {
            isunique = verifyuniqueness(child, name);
            if (not isunique)
            {
                break;
            }
        }
    }
    return isunique;
}
